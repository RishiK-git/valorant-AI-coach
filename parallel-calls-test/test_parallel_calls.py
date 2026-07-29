import sys
import os
import time
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from pipeline.select_frames import select_frames

load_dotenv(PROJECT_ROOT / ".env")
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

FRAMES_DIR = PROJECT_ROOT / "test-frames"
SYSTEM_PROMPT = "Describe what happens across this sequence of Valorant gameplay frames."


def scatter(frames: list[dict], group_size: int) -> list[list[dict]]:
    """
    SCATTER: split the full frame list into independent groups.
    Each group will be sent as its own separate request.
    """
    return [frames[i:i + group_size] for i in range(0, len(frames), group_size)]


def build_parts(frames: list[dict]):
    parts = []
    for frame in frames:
        with open(frame["path"], "rb") as f:
            parts.append(types.Part.from_bytes(data=f.read(), mime_type="image/png"))
    return parts


async def process_group(group_index: int, frames: list[dict], semaphore: asyncio.Semaphore):
    """
    Handles ONE scattered group: builds the request, sends it, times it.
    """
    async with semaphore:
        start = time.perf_counter()
        parts = build_parts(frames)

        response = await client.aio.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=[SYSTEM_PROMPT] + parts,
        )

        elapsed = time.perf_counter() - start
        print(f"  Group {group_index} ({len(frames)} images): {elapsed:.2f}s")
        return group_index, response.text, elapsed


async def gather(groups: list[list[dict]], semaphore: asyncio.Semaphore):
    """
    GATHER: fire off all scattered groups concurrently, wait for every one
    to finish, and collect the results.
    """
    tasks = [
        process_group(i, group, semaphore)
        for i, group in enumerate(groups)
    ]
    results = await asyncio.gather(*tasks)

    # results come back in task-submission order from asyncio.gather,
    # but sort explicitly anyway in case this changes to as_completed later
    results.sort(key=lambda r: r[0])
    return results


async def main():
    all_frames = select_frames(str(FRAMES_DIR), interval_sec=0.25)

    # --- SCATTER ---
    groups = scatter(all_frames, group_size=10)
    print(f"Scattering {len(all_frames)} images into {len(groups)} groups of ~10...\n")

    semaphore = asyncio.Semaphore(5)  # cap concurrent requests

    start = time.perf_counter()

    # --- GATHER ---
    results = await gather(groups, semaphore)

    total_elapsed = time.perf_counter() - start
    slowest = max(results, key=lambda r: r[2])

    print(f"\n--- TIMING ---")
    print(f"Total scatter-gather time for {len(groups)} groups: {total_elapsed:.2f} seconds")
    print(f"Slowest individual group: Group {slowest[0]} at {slowest[2]:.2f}s")

    print(f"\n--- PREVIEW (Group 0) ---")
    print(results[0][1][:300])


if __name__ == "__main__":
    asyncio.run(main())
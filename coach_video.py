import os
import glob
import subprocess
import shutil
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Configure client (make sure GEMINI_API_KEY is set in your environment or .env)
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=gemini_api_key)


def extract_frames_every_n_seconds(video_path: str, output_dir: str, interval_sec: float = 2.0):
    """
    Extracts one frame every `interval_sec` seconds from video_path
    and saves them as PNGs in output_dir.
    """
    os.makedirs(output_dir, exist_ok=True)

    fps = 1 / interval_sec
    output_pattern = os.path.join(output_dir, "frame_%05d.png")

    print(f"Extracting frames from {video_path} every {interval_sec}s...")

    subprocess.run(
        [
            "ffmpeg",
            "-i", video_path,
            "-vf", f"fps={fps}",
            "-q:v", "2",
            output_pattern,
        ],
        check=True,
    )

    print(f"Frames extracted to {output_dir}")


def cleanup_frames(output_dir: str):
    """
    Deletes the extracted frames directory after processing is complete.
    """
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        print(f"Cleaned up {output_dir}")


def load_frames(frames_dir: str, max_frames: int = None):
    """
    Loads all PNG/JPG frames from a directory, sorted in order.
    """
    frame_paths = sorted(glob.glob(os.path.join(frames_dir, "*.png")))
    if max_frames:
        frame_paths = frame_paths[:max_frames]
    return frame_paths


def build_image_parts(frame_paths):
    """
    Reads each frame from disk and wraps it as a Gemini image Part.
    """
    parts = []
    for path in frame_paths:
        with open(path, "rb") as f:
            image_bytes = f.read()
        parts.append(
            types.Part.from_bytes(data=image_bytes, mime_type="image/png")
        )
    return parts


def coach_video_frames(frames_dir: str, system_prompt: str, max_frames: int = None):
    frame_paths = load_frames(frames_dir, max_frames=max_frames)

    if not frame_paths:
        raise ValueError(f"No frames found in {frames_dir}")

    print(f"Sending {len(frame_paths)} frames to Gemini...")

    image_parts = build_image_parts(frame_paths)

    # Combine system prompt + all image parts into one request
    contents = [system_prompt] + image_parts

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=contents,
    )

    return response.text


if __name__ == "__main__":
    VIDEO_PATH = "/Users/rishikallepalli/Projects/valorant-coach-poc/skye-clip2.mp4"
    FRAMES_DIR = "/Users/rishikallepalli/Projects/valorant-coach-poc/output-images"
    INTERVAL_SEC = 2.0

    SYSTEM_PROMPT = """
    You are an expert Valorant gameplay analyst.

    You will be given a sequence of images taken from the SAME engagement in chronological order.

    Treat these images as consecutive frames from a short video.

    Your #1 priority is factual correctness based only on what is visible across the sequence.

    Never:
    - Guess information that is not visible.
    - Invent teammates or enemies.
    - Infer round state (clutch, retake, eco, etc.) unless clearly shown.
    - Describe events that cannot reasonably be concluded from the sequence.

    If something is uncertain, explicitly state that it is uncertain.

    --------------------------------------------------

    Follow this process:

    ## Stage 1: Timeline Observation

    Walk through the sequence in order.

    Describe:
    - How the player's position changes.
    - How crosshair placement changes.
    - How enemy positions change.
    - Utility used (only if clearly visible).
    - Any important changes between frames.

    Only report observations supported by the images.

    --------------------------------------------------

    ## Stage 2: Key Moment

    Identify the single most important decision or action that led toward the outcome of the engagement.

    Explain why this moment mattered more than the others.

    --------------------------------------------------

    ## Stage 3: Coaching

    Using only your observations:

    Provide:
    1. The biggest mistake OR biggest positive play.
    2. Why it mattered using Valorant fundamentals.
    3. One concrete adjustment the player could practice.
    4. One thing the player did well (if applicable).

    Keep the coaching specific, actionable, and concise.

    --------------------------------------------------

    Important:
    If the sequence does not provide enough evidence to reach a conclusion, say so rather than guessing.
    """

    try:
        # Step 1: Extract frames from the video
        extract_frames_every_n_seconds(
            video_path=VIDEO_PATH,
            output_dir=FRAMES_DIR,
            interval_sec=INTERVAL_SEC,
        )

        # Step 2: Send extracted frames to Gemini for coaching
        result = coach_video_frames(
            frames_dir=FRAMES_DIR,
            system_prompt=SYSTEM_PROMPT,
            max_frames=None,  # set a number here if you want to test on a subset first
        )

        print(result)

    finally:
        # Step 3: Clean up frames regardless of success or failure
        cleanup_frames(FRAMES_DIR)
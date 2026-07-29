import os
import glob
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = "Describe what happens across this sequence of Valorant gameplay frames."

def load_images(frames_dir: str):
    paths = sorted(glob.glob(os.path.join(frames_dir, "*.png")))
    parts = []
    for path in paths:
        with open(path, "rb") as f:
            parts.append(types.Part.from_bytes(data=f.read(), mime_type="image/png"))
    return parts

if __name__ == "__main__":
    image_parts = load_images("test-frames")
    print(f"Sending {len(image_parts)} images in ONE request...")

    start = time.perf_counter()

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=[SYSTEM_PROMPT] + image_parts,
    )

    elapsed = time.perf_counter() - start
    print(f"Single big request took {elapsed:.2f} seconds")
    print(response.text[:300])  
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=gemini_api_key)


def build_labeled_image_parts(frames: list[dict]):
    """
    Builds a list of [timestamp_label, image_part, timestamp_label, image_part, ...]
    so the model knows exactly which timestamp each frame corresponds to.
    """
    parts = []
    for frame in frames:
        with open(frame["path"], "rb") as f:
            image_bytes = f.read()

        parts.append(f"Timestamp: {frame['timestamp']}")
        parts.append(
            types.Part.from_bytes(data=image_bytes, mime_type="image/png")
        )
    return parts


def analyze_frames(frames: list[dict], system_prompt: str, response_schema) -> dict:
    """
    Sends the selected, timestamp-labeled frames + system prompt to Gemini
    and returns a parsed object matching response_schema.
    """
    if not frames:
        raise ValueError("No frames provided for analysis")

    labeled_parts = build_labeled_image_parts(frames)
    contents = [system_prompt] + labeled_parts

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=contents,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=response_schema,
        ),
    )

    return response.parsed
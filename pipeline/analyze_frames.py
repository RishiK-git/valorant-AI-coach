import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=gemini_api_key)


def build_image_parts(frame_paths: list[str]):
    parts = []
    for path in frame_paths:
        with open(path, "rb") as f:
            image_bytes = f.read()
        parts.append(
            types.Part.from_bytes(data=image_bytes, mime_type="image/png")
        )
    return parts


def analyze_frames(frame_paths: list[str], system_prompt: str) -> str:
    """
    Sends the selected frames + system prompt to Gemini and returns raw text response.
    """
    if not frame_paths:
        raise ValueError("No frames provided for analysis")

    image_parts = build_image_parts(frame_paths)
    contents = [system_prompt] + image_parts

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=contents,
    )

    return response.text
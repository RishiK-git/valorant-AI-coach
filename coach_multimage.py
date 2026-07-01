import sys
from google import genai
import base64
import os
from dotenv import load_dotenv

load_dotenv()


screenshot1 = "/Users/rishikallepalli/Projects/valorant-coach-poc/test-images/multiframe/Screenshot 2026-07-01 at 5.15.48 PM.png"
screenshot2 = "/Users/rishikallepalli/Projects/valorant-coach-poc/test-images/multiframe/Screenshot 2026-07-01 at 5.16.08 PM.png"
screenshot3 = "/Users/rishikallepalli/Projects/valorant-coach-poc/test-images/multiframe/Screenshot 2026-07-01 at 5.16.32 PM.png"
screenshot4 = "/Users/rishikallepalli/Projects/valorant-coach-poc/test-images/multiframe/Screenshot 2026-07-01 at 5.16.49 PM.png"
screenshot5 = "/Users/rishikallepalli/Projects/valorant-coach-poc/test-images/multiframe/Screenshot 2026-07-01 at 5.17.13 PM.png"
screenshot6 = "/Users/rishikallepalli/Projects/valorant-coach-poc/test-images/multiframe/Screenshot 2026-07-01 at 5.17.31 PM.png"
screenshot7 = "/Users/rishikallepalli/Projects/valorant-coach-poc/test-images/multiframe/Screenshot 2026-07-01 at 5.17.44 PM.png"
screenshot8 = "/Users/rishikallepalli/Projects/valorant-coach-poc/test-images/multiframe/Screenshot 2026-07-01 at 5.17.55 PM.png"

with open(screenshot1, "rb") as image_file:
    image_bytes1 = image_file.read()

with open(screenshot2, "rb") as image_file:
    image_bytes2 = image_file.read()

with open(screenshot3, "rb") as image_file:
    image_bytes3 = image_file.read()

with open(screenshot4, "rb") as image_file:
    image_bytes4 = image_file.read()

with open(screenshot5, "rb") as image_file:
    image_bytes5 = image_file.read()

with open(screenshot6, "rb") as image_file:
    image_bytes6 = image_file.read()

with open(screenshot7, "rb") as image_file:
    image_bytes7 = image_file.read()

with open(screenshot8, "rb") as image_file:
    image_bytes8 = image_file.read()


gemini_api_key = os.getenv("GEMINI_API_KEY")


client = genai.Client(api_key=gemini_api_key)

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


interaction = client.interactions.create(
    model="gemini-3.5-flash",
    input=[
        {"type": "text", "text": SYSTEM_PROMPT},
        {
            "type": "image",
            "data": base64.b64encode(image_bytes1).decode('utf-8'),
            "mime_type": "image/png"
        },
        {
            "type": "image",
            "data": base64.b64encode(image_bytes2).decode('utf-8'),
            "mime_type": "image/png"
        },
        {
            "type": "image",
            "data": base64.b64encode(image_bytes3).decode('utf-8'),
            "mime_type": "image/png"
        },
        {
            "type": "image",
            "data": base64.b64encode(image_bytes4).decode('utf-8'),
            "mime_type": "image/png"
        },
        {
            "type": "image",
            "data": base64.b64encode(image_bytes5).decode('utf-8'),
            "mime_type": "image/png"
        },
        {
            "type": "image",
            "data": base64.b64encode(image_bytes6).decode('utf-8'),
            "mime_type": "image/png"
        },
        {
            "type": "image",
            "data": base64.b64encode(image_bytes7).decode('utf-8'),
            "mime_type": "image/png"
        },
        {
            "type": "image",
            "data": base64.b64encode(image_bytes8).decode('utf-8'),
            "mime_type": "image/png"
        }
    ]
)
print(interaction.output_text)





import sys
from google import genai
import base64
import os
from dotenv import load_dotenv

load_dotenv()

# Check for screenshot path argument
if len(sys.argv) > 1:
    screenshot = sys.argv[1]
else:
    print("No screenshot path provided. Please provide a path to the screenshot as an argument.")
    sys.exit(1)

with open(screenshot, "rb") as image_file:
    image_bytes = image_file.read()

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")


client = genai.Client(api_key=gemini_api_key)

SYSTEM_PROMPT = """Y
You are a Valorant gameplay analyst.

Your #1 priority is factual correctness based only on what is directly visible in the image.

You must NEVER:
- guess agent identities if unclear
- infer round state (e.g., “1vX”, “clutch”, “eco”, “retake”) unless explicitly shown in HUD
- assume enemy positions outside the frame
- invent teammates or unseen players
- describe events not visible in the frame

If something is uncertain, explicitly say: "Not clearly visible"

---

You must follow this 2-stage process:

## Stage 1: OBSERVATION (STRICT)
Only describe what is directly visible in the image.

Rules:
- No coaching
- No interpretation
- No FPS theory
- No assumptions
- Only facts

Format:
- Bullet points
- Short, precise
- Include confidence tags: [HIGH], [MED], [LOW]

---

## Stage 2: COACHING (CONDITIONAL)
Only use observations from Stage 1.

Rules:
- Do NOT introduce new facts
- If Stage 1 is uncertain, coaching must reflect that uncertainty
- Focus on 1–2 highest impact improvements only
- Be specific and actionable

---

## Output format:

### OBSERVATION
...

### COACHING
...
"""


interaction = client.interactions.create(
    model="gemini-3.5-flash",
    input=[
        {"type": "text", "text": SYSTEM_PROMPT},
        {
            "type": "image",
            "data": base64.b64encode(image_bytes).decode('utf-8'),
            "mime_type": "image/jpeg"
        }
    ]
)

print(interaction.output_text)



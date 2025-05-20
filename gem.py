#!/home/bandit/.local/share/gemini/.venv/bin/python3 
#

import os
import argparse
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")

# Model lookup table
MODEL_LOOKUP = {
    "flash": "gemini-2.5-flash-preview-05-20",
    "pro": "gemini-2.5-pro-preview-05-06"
}

# Default model
DEFAULT_MODEL = "flash"

parser = argparse.ArgumentParser(description="Generate text using the Gemini API.")
parser.add_argument("-m", "--model", choices=MODEL_LOOKUP.keys(), default=DEFAULT_MODEL,
                    help="Model to use (short name).")
parser.add_argument("prompt", nargs="+", default="", help="The prompt text.")
args = parser.parse_args()

# Get the full model name from the lookup table
model = MODEL_LOOKUP[args.model]

client = genai.Client(api_key=api_key)

prompt = args.prompt

response = client.models.generate_content(
    model=model,
    contents=prompt,
)

print(response.text)

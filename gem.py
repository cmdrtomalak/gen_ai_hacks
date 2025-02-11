# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "argparse",
#     "google-genai",
# ]
# ///

#!/usr/bin/env python3
#

import os
import argparse
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")

# Model lookup table
MODEL_LOOKUP = {
    "flash": "gemini-1.5-flash",
    "flash2": "gemini-2.0-flash-exp",
    "exp": "gemini-exp-1206",
    "think": "gemini-2.0-flash-thinking-exp-1219"
}

# Default model
DEFAULT_MODEL = "flash2"

parser = argparse.ArgumentParser(description="Generate text using the Gemini API.")
parser.add_argument("-m", "--model", choices=MODEL_LOOKUP.keys(), default=DEFAULT_MODEL,
                    help="Model to use (short name).")
parser.add_argument("-p", "--prompt", nargs="+", help="The prompt text.")
args = parser.parse_args()

# Get the full model name from the lookup table
model = MODEL_LOOKUP[args.model]

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Explain how AI works",
)

print(response.text)

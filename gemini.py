#!/usr/bin/env python3
#

import os
import requests
import argparse
import subprocess
import re
import textwrap

# Model lookup table
MODEL_LOOKUP = {
    "flash": "gemini-1.5-flash",
    "flash2": "gemini-2.0-flash-exp",
    "exp": "gemini-exp-1206",
    "think": "gemini-2.0-flash-thinking-exp-1219"
}

# Default model
DEFAULT_MODEL = "gemini-1.5-flash"


def render_basic_markdown(text):
    # --- Text Wrapping ---
    wrapper = textwrap.TextWrapper(width=80, break_long_words=False)

    # --- Headings (with spacing) ---
    # Add a newline after headings
    text = re.sub(r"^(#+ .+\n)", r"\1\n", text, flags=re.MULTILINE)

    # --- Bold and Italics ---
    text = re.sub(r"\*\*(.+?)\*\*", r"\033[1m\1\033[0m", text)  # Bold
    text = re.sub(r"\*(.+?)\*", r"\033[3m\1\033[0m", text)  # Italics

    # --- Code Spans ---
    text = re.sub(r"`(.+?)`", r"\033[92m\1\033[0m", text)  # Green code

    lines = text.split("\n")
    formatted_lines = []
    for line in lines:
        if line.startswith(("#", " ")):
            # Don't wrap headings or lines starting with spaces (usually code blocks)
            formatted_lines.append(line)
        elif line.startswith("* "):  # Basic unordered list
            formatted_lines.append(textwrap.indent(line, "  "))
        else:
            # Wrap other lines (paragraphs)
            wrapped_lines = wrapper.wrap(line)
            if wrapped_lines:  # Handle empty lines
                formatted_lines.extend(wrapped_lines)
            else:
                formatted_lines.append("")

    return "\n".join(formatted_lines)


def main():
    parser = argparse.ArgumentParser(description="Generate text using the Gemini API.")
    parser.add_argument("-m", "--model", choices=MODEL_LOOKUP.keys(), default=DEFAULT_MODEL,
                        help="Model to use (short name).")
    parser.add_argument("prompt", nargs="+", help="The prompt text.")
    args = parser.parse_args()

    # Get the full model name from the lookup table
    model = MODEL_LOOKUP[args.model]

    # Construct the prompt text
    prompt_text = " ".join(args.prompt)

    # Get the API key from the environment variable
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        exit(1)

    # Construct the API request URL
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

    # Construct the API request payload
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt_text}
                ]
            }
        ]
    }

    # Send the API request
    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Extract the text from the response
        response_json = response.json()
        generated_text = response_json["candidates"][0]["content"]["parts"][0]["text"]

        # Render the basic Markdown
        rendered_markdown = render_basic_markdown(generated_text)
        print(rendered_markdown)

    except requests.exceptions.RequestException as e:
        print(f"Error: API request failed: {e}")
        exit(1)
    except KeyError as e:
        print(f"Error: Invalid response format: {e}")
        exit(1)

if __name__ == "__main__":
    main()

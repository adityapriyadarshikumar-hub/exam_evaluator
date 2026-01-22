import json
import re

def safe_json_load(text: str):
    text = text.strip()
    # Extract JSON from code blocks
    json_match = re.search(r'```(?:json)?\s*\n(.*?)\n```', text, re.DOTALL)
    if json_match:
        text = json_match.group(1).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {repr(text)}")
        raise ValueError("Invalid JSON returned by LLM") from e

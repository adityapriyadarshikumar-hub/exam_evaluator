import json
import re

def safe_json_load(text: str):
    text = text.strip()
    # Remove common prefixes like 'json '
    if text.lower().startswith('json '):
        text = text[5:].strip()
    # Extract JSON from code blocks
    json_match = re.search(r'```(?:json)?\s*\n(.*?)\n```', text, re.DOTALL)
    if json_match:
        text = json_match.group(1).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to extract JSON by finding the first { and last }
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1 and end > start:
            potential_json = text[start:end+1]
            try:
                return json.loads(potential_json)
            except json.JSONDecodeError:
                pass
        print(f"Invalid JSON: {repr(text)}")
        raise ValueError("Invalid JSON returned by LLM")

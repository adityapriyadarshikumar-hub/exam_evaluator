import json

def safe_json_load(text: str):
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {repr(text)}")
        raise ValueError("Invalid JSON returned by LLM") from e

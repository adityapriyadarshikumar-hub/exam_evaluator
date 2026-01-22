from utils.llm_client import call_llm
from utils.json_utils import safe_json_load

def extract_student_info(clean_text: str) -> dict:
    if not clean_text.strip():
        return {"name": "Unknown", "rollno": "Unknown"}
    prompt = f"""
Extract student name and roll number from the text.

Text:
{clean_text}

Return STRICT JSON:
{{
  "name": "string",
  "rollno": "string"
}}
"""
    return safe_json_load(call_llm(prompt))
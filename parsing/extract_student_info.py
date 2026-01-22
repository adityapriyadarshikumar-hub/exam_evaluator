from utils.llm_client import call_llm
from utils.json_utils import safe_json_load

def extract_student_info(clean_text: str) -> dict:
    if not clean_text.strip():
        return {"name": "Unknown", "rollno": "Unknown"}
    prompt = f"""
Extract the student's name and roll number from the exam paper text.

Look for patterns like:
- Name: [name]
- Roll No: [number]
- Student ID: [number]
- etc.

Text:
{clean_text}

Return STRICT JSON:
{{
  "name": "extracted name or Unknown",
  "rollno": "extracted roll or Unknown"
}}

If not found, use "Unknown".
"""
    try:
        return safe_json_load(call_llm(prompt))
    except:
        return {"name": "Unknown", "rollno": "Unknown"}
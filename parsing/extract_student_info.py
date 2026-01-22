from utils.llm_client import call_llm
from utils.json_utils import safe_json_load
import re

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
        return safe_json_load(call_llm(prompt, force_openai=True))
    except:
        return {"name": "Unknown", "rollno": "Unknown"}

def remove_student_info_from_text(clean_text: str) -> str:
    # Remove lines that contain student information patterns
    lines = clean_text.split('\n')
    filtered_lines = []
    patterns = [
        r'^\s*Name\s*:',
        r'^\s*Roll\s*No\s*:',
        r'^\s*Student\s*ID\s*:',
        r'^\s*Roll\s*Number\s*:',
        r'^\s*ID\s*:',
        r'^\s*Student\s*Name\s*:',
        r'Roll\s*No',
        r'Student\s*ID',
        r'Roll\s*No\s*:',
        r'Student\s*ID\s*:'
    ]
    for line in lines:
        if not any(re.search(pattern, line, re.IGNORECASE) for pattern in patterns):
            filtered_lines.append(line)
    return '\n'.join(filtered_lines).strip()
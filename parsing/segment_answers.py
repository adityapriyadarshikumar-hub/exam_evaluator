from utils.llm_client import call_llm
from utils.json_utils import safe_json_load

def segment_answers(clean_text: str) -> dict:
    if not clean_text.strip():
        return {}
    prompt = f"""
You are an exam answer segmentation system.

Task:
- Detect question numbers (like Q1, Q2, Question 1, etc.)
- Group the text for each question's answer
- Ignore student information (name, roll number, etc.) at the top
- Only return the answers segmented by question

TEXT:
{clean_text}

Return ONLY valid JSON in this format:
```json
{{
  "Q1": "answer text for question 1",
  "Q2": "answer text for question 2"
}}
```

Do not include any other text or explanations.
"""
    return safe_json_load(call_llm(prompt))

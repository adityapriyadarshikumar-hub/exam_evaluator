from utils.llm_client import call_llm
from utils.json_utils import safe_json_load

def atomize_rubric(rubric_text: str) -> dict:
    if not rubric_text.strip():
        return {}
    prompt = f"""
Convert the rubric into atomic scoring units per question.

Rules:
- Identify questions (e.g., Q1, Q2)
- For each question, list atomic units
- Each unit: unit_id, description, marks

RUBRIC:
{rubric_text}

Return STRICT JSON like:
{{
  "Q1": [
    {{"unit_id": "Q1a", "description": "...", "marks": 2}},
    ...
  ],
  "Q2": [...]
}}
"""
    result = safe_json_load(call_llm(prompt))
    # Ensure it's a dict with lists
    if not isinstance(result, dict):
        return {}
    return result

from utils.llm_client import call_llm
from utils.json_utils import safe_json_load

def atomize_rubric(rubric_text: str) -> dict:
    if not rubric_text.strip():
        return {}
    prompt = f"""
Parse the exam rubric into questions and their main subparts.

For each question, identify the main subquestions (like a, b, c) and their total marks.

RUBRIC:
{rubric_text}

Return JSON like:
{{
  "Q1": [
    {{"unit_id": "Q1a", "description": "Find the node with key 'c'", "marks": 2}},
    {{"unit_id": "Q1b", "description": "Remove that node from its position", "marks": 4}}
  ]
}}

Keep units at the subquestion level, not individual steps.
"""
    result = safe_json_load(call_llm(prompt))
    # Ensure it's a dict with lists
    if not isinstance(result, dict):
        return {}
    return result

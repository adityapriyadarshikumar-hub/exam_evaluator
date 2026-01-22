from utils.llm_client import call_llm
from utils.json_utils import safe_json_load

def atomize_rubric(rubric_text: str) -> dict:
    if not rubric_text.strip():
        return {}
    prompt = f"""
Convert the rubric into atomic scoring units.

Rules:
- Each unit independently verifiable
- Include unit_id, description, expected_concept, marks

RUBRIC:
{rubric_text}

Return STRICT JSON.
"""
    return safe_json_load(call_llm(prompt))

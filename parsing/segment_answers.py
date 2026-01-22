from utils.llm_client import call_llm
from utils.json_utils import safe_json_load

def segment_answers(clean_text: str) -> dict:
    if not clean_text.strip():
        return {}
    prompt = f"""
You are an exam answer segmentation system.

Task:
- Detect question numbers
- Group text per question

TEXT:
{clean_text}

Return STRICT JSON:
{{ "Q1": "...", "Q2": "..." }}
"""
    return safe_json_load(call_llm(prompt))

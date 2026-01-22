from utils.llm_client import call_llm, compute_similarity
from utils.json_utils import safe_json_load
from utils.logger import logger

def evaluate_unit(question, unit, student_answer):
    prompt = f"""
You are an impartial exam evaluator.

Question:
{question}

Rubric Unit:
{unit}

Student Answer:
{student_answer}

Rules:
- Allow paraphrasing
- Ignore grammar
- No assumptions

Return STRICT JSON:
{{
  "unit_id": "{unit['unit_id']}",
  "score_awarded": number,
  "confidence": 0.0,
  "justification": "short"
}}
"""
    result = safe_json_load(call_llm(prompt))
    result["question"] = question
    # Compute similarity between student answer and rubric unit text
    rubric_text = str(unit)
    try:
        similarity = compute_similarity(student_answer, rubric_text)
    except Exception as e:
        logger.warning(f"Failed to compute similarity: {e}")
        similarity = 0.0
    result["similarity"] = similarity
    return result

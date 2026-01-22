from utils.llm_client import call_llm

def cleanup_ocr_text(raw_text: str, subject: str) -> str:
    prompt = f"""
You are an OCR post-processing engine for exam answer sheets.

Rules:
- Fix OCR errors only
- Do NOT add or remove content
- Preserve equations and symbols

Subject: {subject}

OCR_TEXT:
{raw_text}

Return corrected text only.
"""
    return call_llm(prompt)

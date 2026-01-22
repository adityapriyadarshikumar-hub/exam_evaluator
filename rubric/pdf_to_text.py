from ocr.pdf_to_images import pdf_to_images
from ocr.ocr_engine import run_ocr
from ocr.ocr_cleanup import cleanup_ocr_text

def extract_rubric_text(rubric_pdf_path, subject):
    images = pdf_to_images(rubric_pdf_path)
    raw_text = run_ocr(images)

    # Optional but recommended
    clean_text = cleanup_ocr_text(raw_text, subject)

    return clean_text

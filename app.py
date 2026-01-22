from ocr.pdf_to_images import pdf_to_images
from ocr.ocr_engine import run_ocr
from ocr.ocr_cleanup import cleanup_ocr_text
from parsing.segment_answers import segment_answers
from parsing.rubric_atomizer import atomize_rubric
from evaluation.unit_evaluator import evaluate_unit
from evaluation.confidence_checker import needs_manual_review
from evaluation.score_aggregator import aggregate_scores
from human_review.flagger import flag_student
from rubric.pdf_to_text import extract_rubric_text
from utils.logger import logger


def evaluate_student(student_pdf, rubric_pdf, subject):
    logger.info("Starting evaluation")

    # 1️⃣ Rubric PDF → Text
    rubric_text = extract_rubric_text(rubric_pdf, subject)

    # 2️⃣ Student PDF → OCR
    images = pdf_to_images(student_pdf)
    raw_text = run_ocr(images)
    clean_text = cleanup_ocr_text(raw_text, subject)

    # 3️⃣ Segment answers
    answers = segment_answers(clean_text)

    # 4️⃣ Atomize rubric
    rubric_units = atomize_rubric(rubric_text)

    all_results = []

    # 5️⃣ Unit-wise evaluation
    for q, units in rubric_units.items():
        for unit in units:
            result = evaluate_unit(q, unit, answers.get(q, ""))
            if needs_manual_review(result):
                flag_student(student_pdf, result["justification"])
            all_results.append(result)

    # 6️⃣ Final score
    final_score = aggregate_scores(all_results)
    logger.info(f"Final Score: {final_score}")

    return final_score


if __name__ == "__main__":
    score = evaluate_student(
        student_pdf="data/students/student.pdf",
        rubric_pdf="data/rubrics/rubric.pdf",
        subject="DSA"
    )
    print("FINAL SCORE =", score)

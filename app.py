from ocr.pdf_to_images import pdf_to_images
from ocr.ocr_engine import run_ocr
from ocr.ocr_cleanup import cleanup_ocr_text
from parsing.segment_answers import segment_answers
from parsing.rubric_atomizer import atomize_rubric
from parsing.extract_student_info import extract_student_info
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

    # 3️⃣ Extract student info
    student_info = extract_student_info(clean_text)

    # 4️⃣ Segment answers
    answers = segment_answers(clean_text)

    # 5️⃣ Atomize rubric
    rubric_units = atomize_rubric(rubric_text)

    all_results = []
    question_scores = {}
    question_similarities = {}

    # 6️⃣ Unit-wise evaluation
    for q, units in rubric_units.items():
        question_results = []
        similarities = []
        for unit in units:
            result = evaluate_unit(q, unit, answers.get(q, ""))
            if needs_manual_review(result):
                flag_student(student_pdf, result["justification"])
            question_results.append(result)
            similarities.append(result.get("similarity", 0))
        # Aggregate per question
        q_score = aggregate_scores(question_results)
        question_scores[q] = q_score["total"]  # since aggregate_scores returns dict, take total
        question_similarities[q] = sum(similarities) / len(similarities) if similarities else 0
        all_results.extend(question_results)

    # 7️⃣ Final score
    total_score = aggregate_scores(all_results)["total"]
    logger.info(f"Final Score: {total_score}")

    # 8️⃣ Overall similarity (average)
    overall_similarity = sum(question_similarities.values()) / len(question_similarities) if question_similarities else 0

    # For output, return dict
    result = {
        "name": student_info.get("name", "Unknown"),
        "rollno": student_info.get("rollno", "Unknown"),
        "question_scores": question_scores,
        "total_score": total_score,
        "similarity": overall_similarity
    }

    return result


if __name__ == "__main__":
    result = evaluate_student(
        student_pdf="data/students/student.pdf",
        rubric_pdf="data/rubrics/rubric.pdf",
        subject="DSA"
    )
    print("EVALUATION RESULT =", result)

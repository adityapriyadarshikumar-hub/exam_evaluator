def aggregate_scores(results: list) -> dict:
    question_scores = {}
    total = 0
    for r in results:
        q = r.get("question", "Unknown")
        score = r["score_awarded"]
        if q not in question_scores:
            question_scores[q] = 0
        question_scores[q] += score
        total += score
    return {"question_scores": question_scores, "total": total}

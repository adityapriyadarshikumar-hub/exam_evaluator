def aggregate_scores(results: list) -> float:
    return sum(r["score_awarded"] for r in results)

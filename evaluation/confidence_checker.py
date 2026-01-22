def needs_manual_review(result: dict) -> bool:
    return (
        result["confidence"] < 0.6 or
        "uncertain" in result["justification"].lower()
    )

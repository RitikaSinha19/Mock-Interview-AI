def determine_difficulty(score: int) -> str:
    """
    Determine the next interview difficulty based
    on the candidate's latest score.
    """

    if score <= 3:
        return "easy"

    elif score <= 6:
        return "medium"

    elif score <= 8:
        return "hard"

    else:
        return "hard"
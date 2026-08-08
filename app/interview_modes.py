def get_question_type(
    interview_mode: str,
    question_number: int
) -> str:

    interview_mode = interview_mode.lower()

    if interview_mode == "technical":
        return "technical"

    if interview_mode == "hr":
        return "hr"

    if interview_mode == "behavioral":
        return "behavioral"

    if interview_mode == "mixed":

        sequence = [
            "technical",
            "technical",
            "behavioral",
            "technical",
            "hr",
            "technical"
        ]

        index = (question_number - 1) % len(sequence)

        return sequence[index]

    return "technical"
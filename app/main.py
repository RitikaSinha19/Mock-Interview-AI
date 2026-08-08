from question_generator import (
    generate_question,
    generate_follow_up_question
)

from answer_evaluator import evaluate_answer

from adaptive_engine import determine_next_step

from difficulty_controller import determine_difficulty


def main():

    # ==================================================
    # INTERVIEW CONFIGURATION
    # ==================================================

    role = "Java Backend Developer"
    interview_type = "technical"
    topic = "OOP"
    difficulty = "medium"
    experience = "Fresher"

    # ==================================================
    # INTERVIEW HISTORY
    # ==================================================

    interview_history = []

    previous_questions = []

    # ==================================================
    # STEP 1
    # GENERATE FIRST QUESTION
    # ==================================================

    print("\nGenerating interview question...")

    question_data = generate_question(
        role=role,
        interview_type=interview_type,
        topic=topic,
        difficulty=difficulty,
        experience=experience,
        previous_questions=previous_questions
    )

    question = question_data["question"]

    print("\nInterview Question")
    print("--------------------------------")
    print(question)

    print("\nTopic:", question_data["topic"])
    print("Subtopic:", question_data["subtopic"])
    print("Difficulty:", question_data["difficulty"])

    # ==================================================
    # CANDIDATE ANSWER
    # ==================================================

    candidate_answer = input(
        "\nYour Answer:\n> "
    )

    # ==================================================
    # STEP 2
    # EVALUATE ANSWER
    # ==================================================

    print("\nEvaluating your answer...")

    evaluation = evaluate_answer(
        question=question,
        candidate_answer=candidate_answer,
        question_type=question_data["question_type"],
        topic=question_data["topic"],
        difficulty=question_data["difficulty"]
    )

    # ==================================================
    # DISPLAY EVALUATION
    # ==================================================

    print("\nAI Evaluation")
    print("--------------------------------")

    print(
        "Overall Score:",
        f"{evaluation['score']}/10"
    )

    print(
        "Technical Accuracy:",
        f"{evaluation['technical_accuracy']}/10"
    )

    print(
        "Conceptual Understanding:",
        f"{evaluation['conceptual_understanding']}/10"
    )

    print(
        "Depth:",
        f"{evaluation['depth']}/10"
    )

    print(
        "Communication:",
        f"{evaluation['communication']}/10"
    )

    print("\nStrengths:")

    for strength in evaluation["strengths"]:
        print("-", strength)

    print("\nWeaknesses:")

    for weakness in evaluation["weaknesses"]:
        print("-", weakness)

    print("\nMissing Concepts:")

    for concept in evaluation["missing_concepts"]:
        print("-", concept)

    print("\nFeedback:")
    print(evaluation["feedback"])

    # ==================================================
    # STORE INTERVIEW HISTORY
    # ==================================================

    interview_history.append(
        {
            "question": question,
            "topic": question_data["topic"],
            "subtopic": question_data["subtopic"],
            "difficulty": question_data["difficulty"],
            "score": evaluation["score"]
        }
    )

    previous_questions.append(question)

    # ==================================================
    # STEP 5A
    # DETERMINE NEXT DIFFICULTY
    # ==================================================

    next_difficulty = determine_difficulty(
        evaluation["score"]
    )

    print("\nDifficulty Controller")
    print("--------------------------------")

    print(
        "Current Score:",
        evaluation["score"]
    )

    print(
        "Recommended Difficulty:",
        next_difficulty
    )

    # ==================================================
    # STEP 4
    # ADAPTIVE DECISION
    # ==================================================

    print("\nAdaptive Decision")
    print("--------------------------------")

    next_step = determine_next_step(
        current_question=question,
        current_topic=question_data["topic"],
        current_subtopic=question_data["subtopic"],
        current_difficulty=question_data["difficulty"],
        evaluation=evaluation,
        interview_history=interview_history
    )

    print(
        "Next Action:",
        next_step["next_action"]
    )

    print(
        "Next Topic:",
        next_step["next_topic"]
    )

    print(
        "Next Subtopic:",
        next_step["next_subtopic"]
    )

    print(
        "Next Difficulty:",
        next_step["next_difficulty"]
    )

    print(
        "\nReason:",
        next_step["reason"]
    )

    # ==================================================
    # STEP 5B
    # GENERATE FOLLOW-UP
    # ==================================================

    print("\nGenerating Follow-up Question...")

    follow_up = generate_follow_up_question(
        role=role,
        question=question,
        candidate_answer=candidate_answer,
        evaluation=evaluation
    )

    print("\nFollow-up Question")
    print("--------------------------------")

    print(
        follow_up["question"]
    )

    print("\nFollow-up Reason:")
    print(
        follow_up["reason"]
    )


if __name__ == "__main__":
    main()
import streamlit as st

from question_generator import (
    generate_question,
    generate_follow_up_question
)

from answer_evaluator import evaluate_answer

from adaptive_engine import determine_next_step

from difficulty_controller import determine_difficulty

from interview_modes import get_question_type

from company_profiles import COMPANY_PROFILES


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Interview Mentor",
    page_icon="AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# UI THEME
# DARK BLUE + SKY BLUE + WHITE
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            linear-gradient(
                135deg,
                #04111f 0%,
                #061a2f 50%,
                #082641 100%
            );

        color: #f5f9ff;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    h1 {
        color: #ffffff !important;
        font-weight: 700 !important;
        letter-spacing: -0.8px;
    }

    h2 {
        color: #dff3ff !important;
        font-weight: 650 !important;
    }

    h3 {
        color: #8fd7ff !important;
        font-weight: 600 !important;
    }

    p {
        color: #d8e9f7 !important;
    }

    label {
        color: #cde7f8 !important;
    }

    .stTextInput input,
    .stTextArea textarea {

        background-color: #0a223a !important;

        color: #ffffff !important;

        border: 1px solid #245477 !important;

        border-radius: 9px !important;
    }

    .stTextInput input:focus,
    .stTextArea textarea:focus {

        border-color: #61c7ff !important;

        box-shadow:
            0 0 0 1px #61c7ff !important;
    }

    .stTextArea textarea {
        line-height: 1.6 !important;
    }

    textarea::placeholder,
    input::placeholder {
        color: #7295b0 !important;
    }

    div[data-baseweb="select"] > div {

        background-color: #0a223a !important;

        color: #ffffff !important;

        border: 1px solid #245477 !important;

        border-radius: 9px !important;
    }

    .stButton > button {

        width: 100%;

        background:
            linear-gradient(
                135deg,
                #0878bd,
                #25a8e8
            );

        color: #ffffff;

        border: 1px solid #4fc3f7;

        border-radius: 9px;

        padding: 0.65rem 1rem;

        font-weight: 600;

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease,
            background 0.2s ease;
    }

    .stButton > button:hover {

        background:
            linear-gradient(
                135deg,
                #1597d1,
                #45c3f5
            );

        border-color: #8bdcff;

        color: #ffffff;

        transform: translateY(-1px);

        box-shadow:
            0 7px 22px rgba(
                37,
                168,
                232,
                0.25
            );
    }

    hr {
        border-color: #1b4665 !important;
    }

    [data-testid="stMetric"] {

        background:
            linear-gradient(
                145deg,
                #09243d,
                #0c304f
            );

        border:
            1px solid #225a7d;

        border-radius: 11px;

        padding: 15px;
    }

    [data-testid="stMetricLabel"] {
        color: #86b6d3 !important;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff !important;
    }

    [data-testid="stAlert"] {

        background-color: #09253e !important;

        border:
            1px solid #28709a !important;

        border-radius: 9px !important;

        color: #e5f6ff !important;
    }

    [data-testid="stExpander"] {

        background-color: #071c30;

        border:
            1px solid #194663;

        border-radius: 10px;
    }

    [data-testid="stExpander"] summary {
        color: #9bdfff !important;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.title("AI Interview Mentor")

st.write(
    "Adaptive interview practice that evaluates your answers "
    "and adjusts the next question based on your performance."
)


# ============================================================
# SESSION STATE
# ============================================================

if "question" not in st.session_state:
    st.session_state.question = None

if "question_data" not in st.session_state:
    st.session_state.question_data = None

if "evaluation" not in st.session_state:
    st.session_state.evaluation = None

if "interview_history" not in st.session_state:
    st.session_state.interview_history = []

if "previous_questions" not in st.session_state:
    st.session_state.previous_questions = []

if "next_difficulty" not in st.session_state:
    st.session_state.next_difficulty = "medium"

if "interview_started" not in st.session_state:
    st.session_state.interview_started = False

if "question_number" not in st.session_state:
    st.session_state.question_number = 0

if "last_candidate_answer" not in st.session_state:
    st.session_state.last_candidate_answer = ""

if "follow_up_question" not in st.session_state:
    st.session_state.follow_up_question = None

if "adaptive_decision" not in st.session_state:
    st.session_state.adaptive_decision = None


# ============================================================
# INTERVIEW CONFIGURATION
# ============================================================

st.subheader("Interview Configuration")


role = st.text_input(
    "Target Role",
    value="Java Backend Developer"
)


experience = st.selectbox(
    "Experience Level",
    [
        "Fresher",
        "Junior",
        "Mid-level",
        "Senior"
    ]
)


interview_mode = st.selectbox(
    "Interview Mode",
    [
        "Technical",
        "HR",
        "Behavioral",
        "Mixed",
        "Company Preparation"
    ]
)


# ============================================================
# COMPANY SELECTION
# ============================================================

company = "General"

if interview_mode == "Company Preparation":

    company = st.selectbox(
        "Company Preparation Profile",
        list(COMPANY_PROFILES.keys())
    )


# ============================================================
# TOPIC
# ============================================================

topic = st.text_input(
    "Topic",
    value="OOP"
)


# ============================================================
# STARTING DIFFICULTY
# ============================================================

difficulty = st.selectbox(
    "Starting Difficulty",
    [
        "easy",
        "medium",
        "hard"
    ],
    index=1
)


# ============================================================
# COMPANY CONTEXT
# ============================================================

additional_context = ""

if interview_mode == "Company Preparation":

    company_profile = COMPANY_PROFILES[company]

    additional_context = f"""
Company Preparation Profile

Company:
{company}

Style:
{company_profile["style"]}

Technical Weight:
{company_profile["technical_weight"]}

Behavioral Weight:
{company_profile["behavioral_weight"]}

Configured Difficulty:
{company_profile["difficulty"]}

Important:
This is a configurable preparation profile.
Do not claim that these characteristics represent
the company's actual current hiring process.
Do not claim that the company definitely asks
specific questions.
"""


# ============================================================
# START INTERVIEW
# ============================================================

if st.button("Start Interview"):

    st.session_state.interview_started = True

    st.session_state.evaluation = None

    st.session_state.interview_history = []

    st.session_state.previous_questions = []

    st.session_state.question_number = 1

    st.session_state.last_candidate_answer = ""

    st.session_state.follow_up_question = None

    st.session_state.adaptive_decision = None

    st.session_state.next_difficulty = difficulty


    # --------------------------------------------------------
    # FIRST QUESTION TYPE
    # --------------------------------------------------------

    if interview_mode == "Company Preparation":

        question_type = "technical"

    else:

        question_type = get_question_type(
            interview_mode,
            st.session_state.question_number
        )


    # --------------------------------------------------------
    # GENERATE FIRST QUESTION
    # --------------------------------------------------------

    with st.spinner(
        "Preparing your first question..."
    ):

        question_data = generate_question(
            role=role,
            interview_type=question_type,
            topic=topic,
            difficulty=difficulty,
            experience=experience,
            previous_questions=[],
            additional_context=additional_context
        )


    st.session_state.question_data = question_data

    st.session_state.question = (
        question_data["question"]
    )

    st.rerun()


# ============================================================
# CURRENT INTERVIEW HISTORY
# ============================================================

if st.session_state.interview_history:

    st.divider()

    with st.expander("Interview History"):

        for index, item in enumerate(
            st.session_state.interview_history,
            start=1
        ):

            st.subheader(
                f"Question {index}"
            )

            st.write(
                item["question"]
            )

            st.write("Your Answer")

            st.write(
                item["answer"]
            )

            st.caption(
                f"Type: {item['question_type']} | "
                f"Topic: {item['topic']} | "
                f"Difficulty: {item['difficulty']} | "
                f"Score: {item['score']}/10"
            )

            if index < len(
                st.session_state.interview_history
            ):

                st.divider()


# ============================================================
# CURRENT QUESTION + ANSWER
# ============================================================

if st.session_state.question:

    question_data = st.session_state.question_data

    st.divider()


    # ========================================================
    # TWO COLUMN LAYOUT
    # ========================================================

    question_column, answer_column = st.columns(
        [1, 1],
        gap="large"
    )


    # ========================================================
    # QUESTION
    # ========================================================

    with question_column:

        st.subheader(
            f"Question {st.session_state.question_number}"
        )

        st.write(
            question_data["question"]
        )

        st.caption(
            f"Type: {question_data['question_type']} | "
            f"Topic: {question_data['topic']} | "
            f"Subtopic: {question_data['subtopic']} | "
            f"Difficulty: {question_data['difficulty']}"
        )


    # ========================================================
    # ANSWER
    # ========================================================

    with answer_column:

        st.subheader("Your Answer")

        candidate_answer = st.text_area(
            "Answer",
            height=300,
            placeholder="Type your interview answer here...",
            key=(
                f"answer_box_"
                f"{st.session_state.question_number}"
            ),
            label_visibility="collapsed"
        )


        if st.button("Submit Answer"):

            if not candidate_answer.strip():

                st.warning(
                    "Please provide an answer before submitting."
                )

            else:

                with st.spinner(
                    "Evaluating your answer..."
                ):

                    evaluation = evaluate_answer(
                        question=question_data["question"],
                        candidate_answer=candidate_answer,
                        question_type=(
                            question_data["question_type"]
                        ),
                        topic=question_data["topic"],
                        difficulty=(
                            question_data["difficulty"]
                        )
                    )


                # --------------------------------------------
                # STORE EVALUATION
                # --------------------------------------------

                st.session_state.evaluation = evaluation

                st.session_state.last_candidate_answer = (
                    candidate_answer
                )


                # --------------------------------------------
                # STORE INTERVIEW HISTORY
                # --------------------------------------------

                st.session_state.interview_history.append(
                    {
                        "question": (
                            question_data["question"]
                        ),

                        "answer": candidate_answer,

                        "question_type": (
                            question_data["question_type"]
                        ),

                        "topic": (
                            question_data["topic"]
                        ),

                        "subtopic": (
                            question_data["subtopic"]
                        ),

                        "difficulty": (
                            question_data["difficulty"]
                        ),

                        "score": evaluation["score"]
                    }
                )


                # --------------------------------------------
                # STORE PREVIOUS QUESTION
                # --------------------------------------------

                st.session_state.previous_questions.append(
                    question_data["question"]
                )


                # --------------------------------------------
                # NEXT DIFFICULTY
                # --------------------------------------------

                next_difficulty = determine_difficulty(
                    evaluation["score"]
                )

                st.session_state.next_difficulty = (
                    next_difficulty
                )

                st.session_state.follow_up_question = None

                st.session_state.adaptive_decision = None

                st.rerun()


# ============================================================
# EVALUATION
# ============================================================

if st.session_state.evaluation:

    evaluation = st.session_state.evaluation

    st.divider()

    st.subheader("Answer Evaluation")


    # ========================================================
    # OVERALL SCORE
    # ========================================================

    st.metric(
        "Overall Score",
        f"{evaluation.get('score', 0)}/10"
    )


    # ========================================================
    # SCORE BREAKDOWN
    # ========================================================

    score_col_1, score_col_2 = st.columns(2)


    with score_col_1:

        st.metric(
            "Technical Accuracy",
            f"{evaluation.get('technical_accuracy', '-')}/10"
        )

        st.metric(
            "Conceptual Understanding",
            f"{evaluation.get('conceptual_understanding', '-')}/10"
        )

        st.metric(
            "Depth",
            f"{evaluation.get('depth', '-')}/10"
        )


    with score_col_2:

        st.metric(
            "Communication",
            f"{evaluation.get('communication', '-')}/10"
        )

        st.metric(
            "Relevance",
            f"{evaluation.get('relevance', '-')}/10"
        )

        st.metric(
            "Specificity",
            f"{evaluation.get('specificity', '-')}/10"
        )


    st.metric(
        "Professionalism",
        f"{evaluation.get('professionalism', '-')}/10"
    )


    # ========================================================
    # CONFIDENCE INDICATORS
    # ========================================================

    st.subheader("Confidence Indicators")

    st.write(
        evaluation.get(
            "confidence_indicators",
            "No confidence indicators available."
        )
    )

    st.caption(
        "These indicators are inferred only from "
        "the written response."
    )


    # ========================================================
    # STRENGTHS
    # ========================================================

    st.subheader("Strengths")

    strengths = evaluation.get(
        "strengths",
        []
    )

    if strengths:

        for strength in strengths:

            st.write(
                f"◆ {strength}"
            )

    else:

        st.write(
            "No specific strengths identified."
        )


    # ========================================================
    # WEAKNESSES
    # ========================================================

    st.subheader("Weaknesses")

    weaknesses = evaluation.get(
        "weaknesses",
        []
    )

    if weaknesses:

        for weakness in weaknesses:

            st.write(
                f"◆ {weakness}"
            )

    else:

        st.write(
            "No specific weaknesses identified."
        )


    # ========================================================
    # MISSING CONCEPTS
    # ========================================================

    st.subheader("Missing Concepts")

    missing_concepts = evaluation.get(
        "missing_concepts",
        []
    )

    if missing_concepts:

        for concept in missing_concepts:

            st.write(
                f"◇ {concept}"
            )

    else:

        st.write(
            "No important missing concepts identified."
        )


    # ========================================================
    # FEEDBACK
    # ========================================================

    st.subheader("Feedback")

    st.write(
        evaluation.get(
            "feedback",
            "No feedback available."
        )
    )


    # ========================================================
    # BETTER ANSWER
    # ========================================================

    with st.expander("View Better Answer"):

        st.write(
            evaluation.get(
                "better_answer",
                "No better answer available."
            )
        )


    # ========================================================
    # NEXT DIFFICULTY
    # ========================================================

    st.subheader("Next Difficulty")

    st.info(
        f"The next question will target "
        f"**{st.session_state.next_difficulty}** difficulty."
    )


# ============================================================
# GENERATE NEXT QUESTION
# ============================================================

if st.session_state.evaluation:

    st.divider()

    if st.button("Generate Next Question"):

        evaluation = st.session_state.evaluation

        question_data = st.session_state.question_data


        # ====================================================
        # ADAPTIVE ENGINE
        # ====================================================

        with st.spinner(
            "Determining your next challenge..."
        ):

            next_step = determine_next_step(

                current_question=(
                    question_data["question"]
                ),

                current_topic=(
                    question_data["topic"]
                ),

                current_subtopic=(
                    question_data["subtopic"]
                ),

                current_difficulty=(
                    question_data["difficulty"]
                ),

                evaluation=evaluation,

                interview_history=(
                    st.session_state.interview_history
                )
            )


        st.session_state.adaptive_decision = (
            next_step
        )


        # ====================================================
        # DIFFICULTY
        # ====================================================

        next_difficulty = determine_difficulty(
            evaluation["score"]
        )

        st.session_state.next_difficulty = (
            next_difficulty
        )


        # ====================================================
        # QUESTION NUMBER
        # ====================================================

        next_question_number = (
            st.session_state.question_number + 1
        )


        # ====================================================
        # QUESTION TYPE
        # ====================================================

        if interview_mode == "Company Preparation":

            company_profile = COMPANY_PROFILES[company]

            if (
                company_profile["behavioral_weight"]
                >
                company_profile["technical_weight"]
            ):

                next_question_type = "behavioral"

            else:

                next_question_type = "technical"

        else:

            next_question_type = get_question_type(
                interview_mode,
                next_question_number
            )


        # ====================================================
        # NEXT TOPIC
        # ====================================================

        next_topic = next_step["next_topic"]

        next_subtopic = (
            next_step["next_subtopic"]
        )


        # ====================================================
        # FOLLOW-UP DECISION
        # ====================================================

        ask_follow_up = next_step.get(
            "ask_follow_up",
            False
        )


        if ask_follow_up:

            with st.spinner(
                "Preparing a meaningful follow-up..."
            ):

                follow_up = (
                    generate_follow_up_question(

                        role=role,

                        question=(
                            question_data["question"]
                        ),

                        candidate_answer=(
                            st.session_state
                            .last_candidate_answer
                        ),

                        evaluation=evaluation
                    )
                )


            st.session_state.follow_up_question = (
                follow_up
            )


            next_question_data = {

                "question": (
                    follow_up["question"]
                ),

                "question_type": (
                    question_data["question_type"]
                ),

                "topic": (
                    question_data["topic"]
                ),

                "subtopic": (
                    question_data["subtopic"]
                ),

                "difficulty": (
                    next_difficulty
                )
            }


        else:

            with st.spinner(
                "Generating your next question..."
            ):

                next_question_data = (
                    generate_question(

                        role=role,

                        interview_type=(
                            next_question_type
                        ),

                        topic=next_topic,

                        subtopic=next_subtopic,

                        difficulty=next_difficulty,

                        experience=experience,

                        previous_questions=(
                            st.session_state
                            .previous_questions
                        ),

                        additional_context=(
                            additional_context
                        )
                    )
                )


        # ====================================================
        # UPDATE QUESTION NUMBER
        # ====================================================

        st.session_state.question_number = (
            next_question_number
        )


        # ====================================================
        # STORE NEXT QUESTION
        # ====================================================

        st.session_state.question_data = (
            next_question_data
        )

        st.session_state.question = (
            next_question_data["question"]
        )


        # ====================================================
        # CLEAR PREVIOUS EVALUATION
        # ====================================================

        st.session_state.evaluation = None

        st.rerun()
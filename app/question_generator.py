from groq import Groq
from config import GROQ_API_KEY
import json


# ==================================================
# GROQ CLIENT
# ==================================================

client = Groq(
    api_key=GROQ_API_KEY
)


# ==================================================
# QUESTION SCHEMA
# ==================================================

QUESTION_SCHEMA = {
    "type": "object",

    "properties": {

        "question": {
            "type": "string"
        },

        "question_type": {
            "type": "string",
            "enum": [
                "technical",
                "hr",
                "behavioral",
                "situational"
            ]
        },

        "topic": {
            "type": "string"
        },

        "subtopic": {
            "type": "string"
        },

        "difficulty": {
            "type": "string",
            "enum": [
                "easy",
                "medium",
                "hard"
            ]
        }
    },

    "required": [
        "question",
        "question_type",
        "topic",
        "subtopic",
        "difficulty"
    ],

    "additionalProperties": False
}


# ==================================================
# SYSTEM PROMPT
# ==================================================

SYSTEM_PROMPT = """
You are an expert professional interviewer.

Your job is to conduct realistic interviews.

You are NOT a chatbot.
You are an interviewer.

Interview types:

1. TECHNICAL

- Test technical knowledge and problem solving.
- Prioritize correctness.
- Use conceptual, practical, debugging,
  and scenario-based questions.

2. HR

- Evaluate motivation, communication,
  career goals, strengths, weaknesses,
  professionalism, and self-awareness.
- Avoid unnecessary technical questions.

3. BEHAVIORAL

- Focus on real workplace behavior.
- Use situations involving teamwork,
  conflict, leadership, failure,
  adaptability, ownership, and problem solving.
- Prefer questions that encourage concrete examples.

4. SITUATIONAL

- Present realistic workplace scenarios.
- Ask what the candidate would do and why.

5. MIXED

- Combine technical, HR, and behavioral questions.
- Follow the requested question type for the
  current question.

General rules:

1. Generate exactly ONE interview question.

2. Match the requested role.

3. Match the requested interview type.

4. Match the requested topic when provided.

5. Match the requested subtopic when provided.

6. Match the requested difficulty.

7. Prefer realistic interview questions over
   textbook-style questions.

8. Test understanding and application whenever possible.

9. Do not provide the answer.

10. Do not provide explanations.

11. Do not reveal what the interviewer expects.

12. Avoid vague or generic questions.

13. Do not repeat previously asked questions.

14. If the same concept was already tested,
    create a meaningfully different question
    or explore a closely related concept.

15. For behavioral questions, prefer concrete
    workplace situations.

16. For HR questions, avoid making unsupported
    assumptions about the candidate.

17. For company preparation profiles, treat the
    provided company information as configurable
    simulation guidance only.

18. Never claim that a company definitely asks
    a specific question unless reliable information
    was explicitly provided.

19. Return only the requested structured output.
"""


# ==================================================
# GENERATE INTERVIEW QUESTION
# ==================================================

def generate_question(
    role: str,
    interview_type: str,
    topic: str,
    difficulty: str,
    experience: str,
    subtopic: str = "",
    previous_questions: list = None,
    additional_context: str = ""
):

    if previous_questions is None:
        previous_questions = []


    user_prompt = f"""
Generate one interview question using these requirements.

Role:
{role}

Interview Type:
{interview_type}

Topic:
{topic}

Subtopic:
{subtopic}

Difficulty:
{difficulty}

Candidate Experience:
{experience}

Previously Asked Questions:
{json.dumps(previous_questions, indent=2)}

Additional Interview Context:
{additional_context}

Important:

Do not repeat any previously asked question.

If previous questions tested the same concept,
create a meaningfully different question or test
a closely related concept.

The generated question must match the requested
interview type.
"""


    response = client.chat.completions.create(

        model="openai/gpt-oss-20b",

        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },

            {
                "role": "user",
                "content": user_prompt
            }
        ],

        response_format={
            "type": "json_schema",

            "json_schema": {
                "name": "interview_question",

                "strict": True,

                "schema": QUESTION_SCHEMA
            }
        },

        temperature=0.4
    )


    content = response.choices[0].message.content

    return json.loads(content)


# ==================================================
# GENERATE FOLLOW-UP QUESTION
# ==================================================

def generate_follow_up_question(
    role: str,
    question: str,
    candidate_answer: str,
    evaluation: dict
):

    evaluation_text = json.dumps(
        evaluation,
        indent=2
    )


    user_prompt = f"""
Generate exactly ONE meaningful follow-up
interview question.

Role:
{role}

Original Question:
{question}

Candidate Answer:
{candidate_answer}

Evaluation:
{evaluation_text}

Rules:

1. The follow-up must directly relate to
   the candidate's answer.

2. Use something the candidate said,
   missed, or explained incompletely.

3. Do not repeat the original question.

4. Do not reveal the answer.

5. Do not ask an unrelated question.

6. Prefer a deeper or clarifying question.

7. The question should feel like something
   a real interviewer would naturally ask
   after hearing the candidate's response.

8. If the candidate made a technically
   incorrect claim, the follow-up may
   investigate that claim.

9. For HR or behavioral answers, the
   follow-up may request a concrete example
   or ask about the candidate's reasoning.
"""


    response = client.chat.completions.create(

        model="openai/gpt-oss-20b",

        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },

            {
                "role": "user",
                "content": user_prompt
            }
        ],

        response_format={
            "type": "json_schema",

            "json_schema": {
                "name": "follow_up_question",

                "strict": True,

                "schema": {

                    "type": "object",

                    "properties": {

                        "question": {
                            "type": "string"
                        },

                        "reason": {
                            "type": "string"
                        }
                    },

                    "required": [
                        "question",
                        "reason"
                    ],

                    "additionalProperties": False
                }
            }
        },

        temperature=0.3
    )


    content = response.choices[0].message.content

    return json.loads(content)
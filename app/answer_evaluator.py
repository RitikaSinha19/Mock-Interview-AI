from groq import Groq
from config import GROQ_API_KEY
import json


# --------------------------------------------------
# Groq Client
# --------------------------------------------------

client = Groq(
    api_key=GROQ_API_KEY
)


# --------------------------------------------------
# Evaluation Schema
# --------------------------------------------------

EVALUATION_SCHEMA = {
    "type": "object",

    "properties": {

        # General score
        "score": {
            "type": "integer",
            "minimum": 0,
            "maximum": 10
        },

        # Technical evaluation
        "technical_accuracy": {
            "type": "integer",
            "minimum": 0,
            "maximum": 10
        },

        "conceptual_understanding": {
            "type": "integer",
            "minimum": 0,
            "maximum": 10
        },

        "depth": {
            "type": "integer",
            "minimum": 0,
            "maximum": 10
        },

        # General communication
        "communication": {
            "type": "integer",
            "minimum": 0,
            "maximum": 10
        },

        # HR / Behavioral / Situational
        "relevance": {
            "type": "integer",
            "minimum": 0,
            "maximum": 10
        },

        "specificity": {
            "type": "integer",
            "minimum": 0,
            "maximum": 10
        },

        "professionalism": {
            "type": "integer",
            "minimum": 0,
            "maximum": 10
        },

        # Qualitative evaluation
        "confidence_indicators": {
            "type": "string"
        },

        "strengths": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },

        "weaknesses": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },

        "missing_concepts": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },

        "feedback": {
            "type": "string"
        },

        "better_answer": {
            "type": "string"
        }
    },

    "required": [
        "score",
        "technical_accuracy",
        "conceptual_understanding",
        "depth",
        "communication",
        "relevance",
        "specificity",
        "professionalism",
        "confidence_indicators",
        "strengths",
        "weaknesses",
        "missing_concepts",
        "feedback",
        "better_answer"
    ],

    "additionalProperties": False
}


# --------------------------------------------------
# System Prompt
# --------------------------------------------------

SYSTEM_PROMPT = """
You are an expert professional interview evaluator.

Evaluate the candidate's answer according to the
type of interview question.

For TECHNICAL questions:

Prioritize:

- Technical accuracy
- Conceptual understanding
- Depth
- Problem solving
- Communication

For HR questions:

Prioritize:

- Relevance
- Communication
- Specificity
- Professionalism
- Self-awareness
- Clarity

For BEHAVIORAL questions:

Prioritize:

- Relevance
- Specificity
- Ownership
- Problem solving
- Communication
- Use of concrete examples
- Reflection and learning

For SITUATIONAL questions:

Prioritize:

- Reasoning
- Decision making
- Communication
- Practicality
- Professionalism
- Handling of the situation

For MIXED questions:

Evaluate the answer according to the
actual question type being evaluated.

General rules:

1. Evaluate only the candidate's actual answer.

2. Do not invent information about the candidate.

3. Do not judge personality, appearance, accent,
   background, intelligence, or other irrelevant
   personal characteristics.

4. Distinguish between an incorrect answer
   and an incomplete answer.

5. Identify important missing concepts or details.

6. Prioritize correctness for technical questions.

7. For HR and behavioral questions, prioritize
   relevance, specificity, professionalism,
   communication, and concrete examples.

8. Confidence indicators must be inferred only
   from the candidate's written response.
   Do not claim to measure actual confidence.

9. Provide constructive and specific feedback.

10. Provide a better example answer.

11. Do not reveal information that was not
    required by the original question.

12. Do not give the candidate credit for
    information they did not provide.

13. If the candidate gives an empty or irrelevant
    answer, reflect that appropriately in the score.

14. Return only the requested structured output.
"""


# --------------------------------------------------
# Evaluate Candidate Answer
# --------------------------------------------------

def evaluate_answer(
    question: str,
    candidate_answer: str,
    question_type: str,
    topic: str,
    difficulty: str
):

    user_prompt = f"""
Evaluate the candidate's answer.

Question Type:
{question_type}

Topic:
{topic}

Difficulty:
{difficulty}

Interview Question:
{question}

Candidate Answer:
{candidate_answer}
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
                "name": "answer_evaluation",

                "strict": True,

                "schema": EVALUATION_SCHEMA
            }
        },

        temperature=0.2
    )

    content = response.choices[0].message.content

    return json.loads(content)
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
# ADAPTIVE DECISION SCHEMA
# ==================================================

ADAPTIVE_SCHEMA = {
    "type": "object",

    "properties": {

        "next_action": {
            "type": "string",
            "enum": [
                "reinforce_weakness",
                "continue_topic",
                "increase_difficulty",
                "decrease_difficulty",
                "explore_related_concept"
            ]
        },

        "next_topic": {
            "type": "string"
        },

        "next_subtopic": {
            "type": "string"
        },

        "next_difficulty": {
            "type": "string",
            "enum": [
                "easy",
                "medium",
                "hard"
            ]
        },

        "ask_follow_up": {
            "type": "boolean"
        },

        "reason": {
            "type": "string"
        }
    },

    "required": [
        "next_action",
        "next_topic",
        "next_subtopic",
        "next_difficulty",
        "ask_follow_up",
        "reason"
    ],

    "additionalProperties": False
}


# ==================================================
# SYSTEM PROMPT
# ==================================================

SYSTEM_PROMPT = """
You are an expert adaptive interview engine.

Your job is to decide what the candidate should
face next based on their current answer and
previous interview performance.

You are NOT the interviewer asking the question.

You are the decision engine behind the interviewer.

Your decisions should consider:

- Current question
- Current topic
- Current subtopic
- Current difficulty
- Candidate score
- Technical accuracy
- Conceptual understanding
- Depth
- Communication
- Relevance
- Specificity
- Professionalism
- Strengths
- Weaknesses
- Missing concepts
- Previous interview history

Rules:

1. If the candidate performs poorly, reinforce the
   weak concept or move to an easier related concept.

2. If the candidate performs at an average level,
   continue with a related concept or moderately
   challenging question.

3. If the candidate performs strongly, gradually
   increase difficulty or explore a deeper related
   concept.

4. Do not repeatedly test the exact same question.

5. Do not unnecessarily repeat the same concept
   unless the candidate demonstrated weakness.

6. Consider missing concepts when deciding what
   should come next.

7. The next topic should be relevant to the current
   topic and candidate performance.

8. The next subtopic should be specific whenever
   possible.

9. Choose a realistic next difficulty.

10. Decide whether a meaningful follow-up question
    would improve the interview.

11. Set ask_follow_up to true ONLY when the
    candidate's answer contains an important gap,
    incomplete explanation, interesting claim,
    ambiguity, or opportunity for useful deeper
    questioning.

12. Set ask_follow_up to false when moving to a
    different concept would be more useful.

13. For HR and behavioral questions, consider
    relevance, specificity, communication,
    professionalism, examples, ownership,
    and reasoning.

14. Do not invent information about the candidate.

15. Return only the requested structured output.
"""


# ==================================================
# DETERMINE NEXT STEP
# ==================================================

def determine_next_step(
    current_question: str,
    current_topic: str,
    current_subtopic: str,
    current_difficulty: str,
    evaluation: dict,
    interview_history: list
):

    evaluation_text = json.dumps(
        evaluation,
        indent=2
    )

    history_text = json.dumps(
        interview_history,
        indent=2
    )


    # --------------------------------------------------
    # USER PROMPT
    # --------------------------------------------------

    user_prompt = f"""
Determine the next interview step.

Current Question:
{current_question}

Current Topic:
{current_topic}

Current Subtopic:
{current_subtopic}

Current Difficulty:
{current_difficulty}

Current Evaluation:
{evaluation_text}

Previous Interview History:
{history_text}

Decide:

1. What should the next action be?
2. What topic should be tested next?
3. What subtopic should be tested next?
4. What difficulty should be used?
5. Should the interviewer ask a meaningful
   follow-up question?
6. Why is this the appropriate next step?

Remember:

- Do not repeat the exact question.
- Reinforce weaknesses when necessary.
- Increase difficulty when the candidate performs well.
- Decrease difficulty when the candidate struggles.
- Use follow-ups only when they add value.
"""


    # --------------------------------------------------
    # GROQ REQUEST
    # --------------------------------------------------

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
                "name": "adaptive_decision",

                "strict": True,

                "schema": ADAPTIVE_SCHEMA
            }
        },

        temperature=0.2
    )


    # --------------------------------------------------
    # PARSE RESPONSE
    # --------------------------------------------------

    content = response.choices[0].message.content

    return json.loads(content)
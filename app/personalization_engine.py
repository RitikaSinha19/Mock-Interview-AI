from groq import Groq
from config import GROQ_API_KEY

import json


client = Groq(
    api_key=GROQ_API_KEY
)


PERSONALIZATION_SCHEMA = {
    "type": "object",
    "properties": {

        "priority_topics": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },

        "topics_to_reduce": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },

        "recommended_difficulty": {
            "type": "string",
            "enum": [
                "easy",
                "medium",
                "hard"
            ]
        },

        "reason": {
            "type": "string"
        }
    },

    "required": [
        "priority_topics",
        "topics_to_reduce",
        "recommended_difficulty",
        "reason"
    ],

    "additionalProperties": False
}


SYSTEM_PROMPT = """
You are an AI interview personalization engine.

Your job is to analyze a candidate's previous
interview performance and recommend what they
should practice next.

Rules:

1. Prioritize consistently weak topics.
2. Consider average performance, not just one score.
3. Consider missing concepts.
4. Avoid spending too much time on consistently
   strong topics.
5. Do not completely ignore strong topics.
6. Recommend a realistic interview difficulty.
7. Do not invent performance data.
8. Use only the provided candidate memory.
9. Return only the requested structured output.
"""


def generate_personalization(memory):

    memory_text = json.dumps(
        memory,
        indent=2
    )

    user_prompt = f"""
Analyze this candidate's interview history:

{memory_text}

Determine:

1. Which topics should receive priority?
2. Which strong topics should receive less focus?
3. What difficulty should the next interview use?
4. Why?

Provide a concise recommendation.
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
                "name": "personalization_strategy",
                "strict": True,
                "schema": PERSONALIZATION_SCHEMA
            }
        },

        temperature=0.2
    )

    content = response.choices[0].message.content

    return json.loads(content)
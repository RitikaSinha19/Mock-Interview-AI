import json
import os


MEMORY_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "candidate_memory.json"
)


def create_empty_memory():

    return {
        "candidate_profile": {
            "role": "",
            "experience": ""
        },
        "topics": {},
        "missing_concepts": {},
        "interview_history": []
    }


def load_memory():

    if not os.path.exists(MEMORY_FILE):

        return create_empty_memory()

    try:

        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except (json.JSONDecodeError, OSError):

        return create_empty_memory()


def save_memory(memory):

    os.makedirs(
        os.path.dirname(MEMORY_FILE),
        exist_ok=True
    )

    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            memory,
            file,
            indent=4
        )



def update_topic_performance(
    memory,
    topic,
    score,
    missing_concepts
):

    if topic not in memory["topics"]:

        memory["topics"][topic] = {
            "attempts": 0,
            "average_score": 0,
            "strength": "unknown"
        }

    topic_data = memory["topics"][topic]

    old_attempts = topic_data["attempts"]
    old_average = topic_data["average_score"]

    new_attempts = old_attempts + 1

    new_average = (
        (old_average * old_attempts) + score
    ) / new_attempts

    topic_data["attempts"] = new_attempts

    topic_data["average_score"] = round(
        new_average,
        2
    )

    if new_average <= 4:

        topic_data["strength"] = "weak"

    elif new_average <= 6:

        topic_data["strength"] = "developing"

    elif new_average <= 8:

        topic_data["strength"] = "good"

    else:

        topic_data["strength"] = "strong"


    if topic not in memory["missing_concepts"]:

        memory["missing_concepts"][topic] = []

    for concept in missing_concepts:

        if concept not in memory["missing_concepts"][topic]:

            memory["missing_concepts"][topic].append(
                concept
            )



def add_interview_record(
    memory,
    topic,
    score,
    difficulty
):

    memory["interview_history"].append(
        {
            "topic": topic,
            "score": score,
            "difficulty": difficulty
        }
    )





def update_candidate_profile(
    memory,
    role,
    experience
):

    memory["candidate_profile"]["role"] = role

    memory["candidate_profile"]["experience"] = (
        experience
    )
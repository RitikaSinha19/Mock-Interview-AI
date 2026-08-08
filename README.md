# AI Interview Mentor

An adaptive AI-powered interview practice platform that simulates realistic technical, HR, and behavioral interviews.

The system evaluates a candidate's responses, identifies strengths and weaknesses, adapts question difficulty, generates meaningful follow-up questions, and selects subsequent questions based on previous performance.

---

## Overview

Traditional interview preparation often relies on static question lists. **AI Interview Mentor** takes a different approach by treating the interview as a dynamic conversation.

Instead of repeatedly asking predefined questions, the AI analyzes each response and decides what the candidate should be asked next.

### Core Flow

```text
Candidate
    ↓
Interview Question
    ↓
Candidate Answer
    ↓
AI Evaluation
    ↓
Adaptive Decision
    ↓
Difficulty Adjustment
    ↓
Follow-up / New Question
    ↓
Repeat
```

The goal is to make every interview session adaptive rather than a fixed sequence of questions.

---

## Features

### Adaptive Interviewing

The AI considers the candidate's previous performance when selecting the next question.

For example:

```text
Weak performance
      ↓
Related concept
      ↓
Easier question

Average performance
      ↓
Related concept
      ↓
Medium question

Strong performance
      ↓
Deeper concept
      ↓
Harder question
```

---

### Technical Interviews

Supports interview preparation across topics such as:

* Java
* OOP
* Collections
* Exception Handling
* Multithreading
* Java 8+
* Spring Boot
* Spring Security
* REST APIs
* JPA / Hibernate
* SQL
* DBMS
* Operating Systems
* Computer Networks
* DSA
* System Design
* Programming Fundamentals

New topics can be introduced without changing the core AI architecture.

---

### HR & Behavioral Interviews

Supports questions involving:

* Tell me about yourself
* Strengths and weaknesses
* Leadership
* Teamwork
* Conflict resolution
* Failure
* Problem solving
* Communication
* Adaptability
* Career goals
* Why should we hire you?
* Why this company?
* Situational questions

Behavioral questions are designed around realistic workplace situations rather than simple random question generation.

---

## Interview Modes

### Technical

Focuses primarily on technical knowledge, conceptual understanding, and application.

### HR

Focuses on communication, motivation, professionalism, career goals, and self-awareness.

### Behavioral

Focuses on workplace experiences such as teamwork, conflict, leadership, failure, and problem solving.

### Mixed

Combines technical, HR, and behavioral questions.

Example sequence:

```text
Technical
Technical
Behavioral
Technical
HR
Technical
```

### Company Preparation

Provides configurable preparation profiles for companies such as:

* Amazon
* Microsoft
* Google
* EY
* TCS
* Infosys
* Accenture

Company profiles are treated as configurable simulation characteristics rather than claims about a company's actual current interview process.

---

## AI Answer Evaluation

After every answer, the AI evaluates the response using structured output.

### Evaluation Criteria

For technical questions:

* Overall score
* Technical accuracy
* Conceptual understanding
* Depth
* Communication
* Confidence indicators
* Strengths
* Weaknesses
* Missing concepts
* Feedback
* Better answer

For HR and behavioral questions, the evaluation also considers factors such as:

* Relevance
* Specificity
* Professionalism
* Communication
* Concrete examples
* Ownership
* Reasoning

---

## Follow-up Questions

The system can generate meaningful follow-up questions based on the candidate's actual response.

Example:

```text
Interviewer:
Explain dependency injection.

Candidate:
Dependency injection means providing dependencies
instead of creating them.

AI:
Why is constructor injection generally preferred
over field injection?
```

The system does not force a follow-up after every answer.

A follow-up is generated when the adaptive engine determines that the candidate's response contains an important gap, incomplete explanation, ambiguity, or useful opportunity for deeper questioning.

---

## Question Repetition Prevention

The system maintains awareness of previously asked questions during the current interview.

It attempts to avoid:

```text
Question 1:
What is polymorphism?

Question 2:
What is polymorphism?
```

Instead, it can explore the same concept differently:

```text
Question 1:
What is polymorphism?

Question 2:
How does runtime polymorphism work in Java?

Question 3:
How does method overriding demonstrate
runtime polymorphism?
```

This allows the AI to track concepts rather than simply repeating question text.

---

## Structured AI Responses

The AI uses structured JSON schemas for important operations.

Example question output:

```json
{
  "question": "Explain runtime polymorphism in Java.",
  "question_type": "technical",
  "topic": "OOP",
  "subtopic": "Polymorphism",
  "difficulty": "medium"
}
```

Example adaptive decision:

```json
{
  "next_action": "reinforce_weakness",
  "next_topic": "OOP",
  "next_subtopic": "Runtime Polymorphism",
  "next_difficulty": "easy",
  "ask_follow_up": true,
  "reason": "The candidate gave a basic definition but did not explain runtime method resolution."
}
```

Structured responses help make the AI pipeline predictable and easier to integrate with application logic.

---

## Personalization

The system considers information such as:

* Target role
* Experience level
* Previous questions
* Previous answers
* Previous scores
* Strong topics
* Weak topics
* Frequently missed concepts
* Practiced concepts
* Interview history
* Current difficulty

The current interview maintains its question and answer history in Streamlit session state.

Longer-term candidate information can be maintained separately for personalization.

---

## Architecture

```text
                    Streamlit UI
                         │
                         ▼
                Question Generator
                         │
                         ▼
                 Interview Question
                         │
                         ▼
                   Candidate Answer
                         │
                         ▼
                  Answer Evaluator
                         │
                         ▼
                  Adaptive Engine
                    /          \
                   /            \
                  ▼              ▼
          Follow-up         New Question
                                │
                                ▼
                       Difficulty Controller
                                │
                                ▼
                         Question Generator
```

---

## Project Structure

```text
AI-Interview-Mentor/
│
├── app/
│   │
│   ├── adaptive_engine.py
│   ├── answer_evaluator.py
│   ├── company_profiles.py
│   ├── config.py
│   ├── difficulty_controller.py
│   ├── interview_modes.py
│   ├── main.py
│   ├── question_generator.py
│   └── streamlit_app.py
│
├── data/
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Technology Stack

### AI / GenAI

* Python
* Groq API
* `openai/gpt-oss-20b`
* Structured JSON Schema responses
* Prompt engineering
* Adaptive decision making

### Interface

* Streamlit

### Development

* Git
* GitHub
* Python virtual environment

The project intentionally keeps the AI layer independent from a larger backend architecture so that the core GenAI functionality can be developed and understood incrementally.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Interview-Mentor.git
```

```bash
cd AI-Interview-Mentor
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the API key

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

Do not commit the `.env` file to GitHub.

### 5. Run the application

From the project root:

```bash
streamlit run app/streamlit_app.py
```

---

## Environment Variables

The project expects:

```text
GROQ_API_KEY
```

Example:

```env
GROQ_API_KEY=your_api_key_here
```

Keep API keys private and never commit them to source control.

---

## Development Roadmap

The AI functionality is being developed incrementally.

```text
1. Question Generation          ✓
2. Answer Evaluation            ✓
3. Structured AI Output         ✓
4. Adaptive Question Selection  ✓
5. Difficulty + Follow-ups      ✓
6. Personalization + Memory     ✓
7. Interview Modes              ✓
8. Final Interview Report       → Next
```

The project intentionally avoids adding unnecessary infrastructure before the core AI behavior is stable.

---

## AI Reliability Principles

The system is designed to:

* Avoid revealing answers before the candidate responds
* Avoid exact question repetition
* Evaluate the actual candidate response
* Distinguish incomplete answers from incorrect answers
* Avoid judging appearance, accent, background, or intelligence
* Use structured outputs where possible
* Handle unexpected responses gracefully
* Avoid unsupported claims about company interview processes
* Treat company preparation profiles as configurable simulations

---

## Why I Built This

This project is designed as a practical exploration of **Generative AI application development**.

Rather than building a simple chatbot around an LLM API, the project focuses on:

* Prompt engineering
* Structured outputs
* AI evaluation
* Adaptive decision making
* Context management
* Personalization
* Dynamic question generation
* Multi-stage LLM workflows

The goal is to understand how individual AI capabilities can be combined into a reliable application workflow.

---

## Current Status

**Active Development**

The core adaptive interview engine is functional, including:

* Technical interviews
* HR interviews
* Behavioral interviews
* Mixed interviews
* Company preparation profiles
* Structured question generation
* Answer evaluation
* Adaptive question selection
* Difficulty adjustment
* AI-generated follow-up questions
* Current-session interview history
* Streamlit interface

The next major feature is the final interview summary and performance report.

---

## Author

Built as a hands-on GenAI project to explore adaptive AI systems and practical LLM application development.

```
```

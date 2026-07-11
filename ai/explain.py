from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


def explain_answer(question,
                   option_a,
                   option_b,
                   option_c,
                   option_d,
                   correct_answer,
                   student_answer):
    prompt = f"""
    You are a friendly teacher helping a student learn.

    Question:
    {question}

    Options:
    A. {option_a}
    B. {option_b}
    C. {option_c}
    D. {option_d}

    Student's Answer:
    {student_answer}

    Correct Answer:
    {correct_answer}

    Give a short explanation (maximum 60 words).

    If the student was wrong:
    - Explain why their answer is incorrect.
    - Explain why the correct answer is right.

    If the student was correct:
    - Congratulate them briefly.
    - Explain why the answer is correct.

    Use simple English suitable for secondary school students.
    """

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content
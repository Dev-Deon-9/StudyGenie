from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


def explain_answer(
    question,
    option_a,
    option_b,
    option_c,
    option_d,
    correct_answer,
    student_answer,
):
    prompt = f"""
You are a study tutor.

Question:
{question}

Options:
A. {option_a}
B. {option_b}
C. {option_c}
D. {option_d}

Student Answer:
{student_answer}

Correct Answer:
{correct_answer}

Reply ONLY in one of these formats.

If the student is correct:

✅ Correct!

💡 Why:
Explain in 1 or 2 short sentences why the answer is correct.

If the student is wrong:

❌ Incorrect!

✅ Correct Answer: {correct_answer}

💡 Why:
Explain in 1 or 2 short sentences why the correct answer is correct.

Rules:
- Maximum 40 words.
- Do NOT explain the wrong options.
- Do NOT add extra facts.
- Do NOT give study tips.
- Do NOT write long paragraphs.
- Keep it short, simple, and easy for secondary school students.
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
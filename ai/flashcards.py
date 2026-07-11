from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


def generate_flashcards(text):

    prompt = f"""
You are an expert teacher.

Read the study material below.

Create between 10 and 20 flashcards depending on the amount of important content.

Rules:
- Focus on key concepts.
- Keep answers under 40 words.
- Do not create duplicates.

Format EXACTLY like this:

Topic:
Question:
Answer:

Study Material:

{text}
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
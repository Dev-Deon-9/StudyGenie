import json
from ai.groq_client import client
from ai.prompts import QUIZ_PROMPT


def generate_quiz(pdf_text):
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "system",
                "content": QUIZ_PROMPT
            },
            {
                "role": "user",
                "content": pdf_text
            }
        ],
        temperature=0.5,
    )

    return json.loads(response.choices[0].message.content)
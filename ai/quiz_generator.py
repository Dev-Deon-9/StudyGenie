import json
from ai.groq_client import client
from ai.prompts import QUIZ_PROMPT


def generate_quiz(pdf_text):
    response = client.chat.completions.create(
        model="moonshotai/kimi-k2-instruct",
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

    content = response.choices[0].message.content

    print("===== GROQ RESPONSE =====")
    print(content)
    print("=========================")

    return json.loads(content)
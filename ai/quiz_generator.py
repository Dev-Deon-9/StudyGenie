import json
import re
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
        temperature=0.3,
    )

    content = response.choices[0].message.content.strip()

    print("===== GROQ RESPONSE =====")
    print(content)
    print("=========================")

    # Try normal JSON parsing first
    try:
        from ai.quiz_parser import parse_quiz

        content = response.choices[0].message.content

        return parse_quiz(content)


    except json.JSONDecodeError:
        pass

    # If Groq wrapped the JSON with extra text, extract only the array
    match = re.search(r"\[.*\]", content, re.DOTALL)

    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    raise Exception("Groq returned invalid JSON. Check the printed response above.")
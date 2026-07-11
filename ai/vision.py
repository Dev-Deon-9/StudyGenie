import base64
from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


def read_note(image_path):
    """
    Reads a note image using Groq Vision
    and returns clean extracted text.
    """

    with open(image_path, "rb") as image:
        image_data = base64.b64encode(image.read()).decode("utf-8")

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """
Extract every readable word from this study note.

Rules:
- Ignore decorations.
- Ignore page numbers.
- Preserve headings.
- Preserve bullet points.
- Preserve numbering.
- Correct obvious OCR mistakes.
- Return ONLY the extracted note.
Do not summarize.
Do not explain.
"""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_data}"
                        }
                    }
                ]
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()
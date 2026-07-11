QUIZ_PROMPT = """
You are an expert teacher.

Generate EXACTLY 30 multiple-choice questions from the study material.

Return ONLY valid JSON.

The format must be:

[
  {
    "question": "...",
    "option_a": "...",
    "option_b": "...",
    "option_c": "...",
    "option_d": "...",
    "correct_answer": "A"
  }
]

Rules:
- Exactly 30 questions.
- Exactly 4 options.
- Correct answer must be A, B, C, or D.
- No explanations.
- No markdown.
- No `json.
- Output ONLY the JSON array.
"""
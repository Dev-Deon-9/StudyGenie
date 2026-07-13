QUIZ_PROMPT = """
You are a quiz generator.

Your task is to generate EXACTLY 30 multiple-choice questions.

IMPORTANT:
- Return ONLY a valid JSON array.
- Do NOT write any text before or after the JSON.
- Do NOT use Markdown.
- Do NOT wrap the JSON inside `json.
- Every object must contain ALL six keys.
- Do NOT duplicate keys.
- Do NOT duplicate questions.
- Use double quotes for every key and value.
- Separate every object with a comma.
- Ensure the final JSON can be parsed by Python's json.loads().

Each object MUST follow this exact format:

{
  "question": "Question here",
  "option_a": "Option A",
  "option_b": "Option B",
  "option_c": "Option C",
  "option_d": "Option D",
  "correct_answer": "A"
}

Return ONLY one JSON array containing exactly 30 objects.
"""
from ai.quiz_generator import generate_quiz

text = """
Python is a programming language.

It is easy to learn.

Python is used for AI, web development,
automation, and data science.
"""

quiz = generate_quiz(text)

print(quiz)
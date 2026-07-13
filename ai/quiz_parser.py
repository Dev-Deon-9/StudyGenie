import re

def parse_quiz(text):
    quizzes = []

    pattern = re.compile(
        r"Question:\s*(.*?)\n"
        r"A\.\s*(.*?)\n"
        r"B\.\s*(.*?)\n"
        r"C\.\s*(.*?)\n"
        r"D\.\s*(.*?)\n"
        r"Answer:\s*([ABCD])",
        re.DOTALL
    )

    for match in pattern.finditer(text):
        quizzes.append({
            "question": match.group(1).strip(),
            "option_a": match.group(2).strip(),
            "option_b": match.group(3).strip(),
            "option_c": match.group(4).strip(),
            "option_d": match.group(5).strip(),
            "correct_answer": match.group(6).strip(),
        })

    return quizzes
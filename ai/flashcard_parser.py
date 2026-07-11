import re


def parse_flashcards(text):
    flashcards = []

    pattern = re.findall(
        r"Topic:\s*(.*?)\s*Question:\s*(.*?)\s*Answer:\s*(.*?)(?=Topic:|$)",
        text,
        re.DOTALL
    )

    for topic, question, answer in pattern:
        flashcards.append({
            "topic": topic.strip(),
            "question": question.strip(),
            "answer": answer.strip()
        })

    return flashcards
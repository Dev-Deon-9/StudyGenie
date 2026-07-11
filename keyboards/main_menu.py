from telegram import ReplyKeyboardMarkup


def main_menu():
    keyboard = [
        ["📄 Upload PDF"],
        ["🖼️ Upload Notes"],
        ["📝 Take Quiz"],
        ["🔄 Retake Quiz"],
        ["🃏 Flashcards"],
        ["📊 Progress"],
        ["❓ Help"]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )
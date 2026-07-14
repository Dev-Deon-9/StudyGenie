from telegram import ReplyKeyboardMarkup


def main_menu():
    keyboard = [
        ["📄 Upload PDF"],
        ["🖼️ Upload Notes"],
        ["📝 Take Quiz"],
        ["🔄 Retake Quiz"],
        ["📊 Progress"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )
import os

from telegram import Update
from telegram.ext import ContextTypes

from database.pdf_database import save_pdf
from handlers.pdf_reader import extract_text
from ai.quiz_generator import generate_quiz

from database.quiz_database import (
    save_quiz,
    delete_old_quiz,
    start_progress,
)

from database.database import add_pdf_upload


async def ask_for_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📄 Please send me the PDF you want to turn into a quiz."
    )


async def receive_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document

    file = await context.bot.get_file(document.file_id)

    telegram_id = update.effective_user.id
    new_file_name = f"{telegram_id}_{document.file_name}"

    os.makedirs("uploads", exist_ok=True)
    os.makedirs("uploads/notes", exist_ok=True)

    save_path = os.path.join("uploads", new_file_name)

    await file.download_to_drive(save_path)

    text = extract_text(save_path)

    # Limit the amount of text sent to the AI
    text = text[:12000]

    questions = generate_quiz(text)[:30]

    print(f"Generated {len(questions)} questions")

    delete_old_quiz(telegram_id)
    start_progress(telegram_id)

    for index, q in enumerate(questions, start=1):
        save_quiz(
            telegram_id,
            index,
            q["question"],
            q["option_a"],
            q["option_b"],
            q["option_c"],
            q["option_d"],
            q["correct_answer"]
        )

    print("Quiz saved successfully!")

    save_pdf(
        telegram_id,
        new_file_name,
        save_path
    )

    add_pdf_upload(telegram_id)

    await update.message.reply_text(
        f"✅ PDF saved successfully!\n\n📄 {new_file_name}"
    )
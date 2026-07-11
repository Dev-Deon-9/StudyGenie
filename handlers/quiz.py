from telegram import Update
from telegram.ext import ContextTypes
from database.quiz_database import (
    get_progress,
    get_question,
    start_progress,
    total_questions,
)


async def take_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id

    progress = get_progress(telegram_id)

    if not progress:
        start_progress(telegram_id)
        current_question = 1
        score = 0
    else:
        current_question, score = progress

    question = get_question(telegram_id, current_question)

    if not question:
        await update.message.reply_text(
            "❌ You don't have any quizzes yet.\n\nPlease upload a PDF first."
        )
        return

    q, a, b, c, d, correct_answer = question

    await update.message.reply_text(
        f"""📝 Question {current_question}/{total_questions(telegram_id)}

{q}

A. {a}
B. {b}
C. {c}
D. {d}
"""
    )
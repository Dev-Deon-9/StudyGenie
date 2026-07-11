from telegram import Update
from telegram.ext import ContextTypes

from database.quiz_database import (
    start_progress,
    total_questions,
)
from handlers.quiz import take_quiz


async def retake_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id

    if total_questions(telegram_id) == 0:
        await update.message.reply_text(
            "❌ You don't have any quiz yet.\n\nPlease upload a PDF first."
        )
        return

    start_progress(telegram_id)

    await update.message.reply_text(
        "🔄 Quiz restarted!\n\nGood luck! 🍀"
    )

    await take_quiz(update, context)
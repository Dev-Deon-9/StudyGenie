from telegram import Update
from telegram.ext import ContextTypes

from database.quiz_database import (
    get_progress,
    total_questions,
)


async def show_progress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id

    progress = get_progress(telegram_id)

    if not progress:
        await update.message.reply_text(
            "📊 You haven't started a quiz yet.\n\nUpload a PDF first."
        )
        return

    current_question, score = progress
    total = total_questions(telegram_id)

    percentage = (score / total) * 100 if total else 0

    if percentage >= 80:
        remark = "🌟 Excellent!"
    elif percentage >= 60:
        remark = "👏 Good Job!"
    elif percentage >= 40:
        remark = "📚 Keep Practicing!"
    else:
        remark = "💪 Don't Give Up!"

    if current_question > total:
        await update.message.reply_text(
            f"""📊 Your Progress

    🏁 Quiz Status: Completed

    📊 Final Score: {score}/{total}
    📈 Percentage: {percentage:.1f}%

    {remark}

    Press 🔄 Retake Quiz to try again.
    """
        )
    else:
        await update.message.reply_text(
            f"""📊 Your Progress

    📝 Current Question: {current_question}/{total}

    ✅ Score: {score}

    📈 Percentage: {percentage:.1f}%

    Keep going! 💪
    """
        )
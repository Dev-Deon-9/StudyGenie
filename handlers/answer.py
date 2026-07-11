from telegram import Update
from telegram.ext import ContextTypes
from ai.explain import explain_answer
from database.quiz_database import (
    get_progress,
    get_question,
    update_progress,
    total_questions,
)

from handlers.quiz import take_quiz


async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("✅ check_answer() called")
    telegram_id = update.effective_user.id
    answer = update.message.text.strip().upper()

    if answer not in ["A", "B", "C", "D"]:
        return

    progress = get_progress(telegram_id)

    if not progress:
        return

    current_question, score = progress

    question = get_question(telegram_id, current_question)

    if not question:
        await update.message.reply_text("❌ Question not found.")
        return

    q, a, b, c, d, correct_answer = question

    if answer == correct_answer:
        score += 1
        await update.message.reply_text("✅ Correct!")
    else:
        await update.message.reply_text(
            f"❌ Incorrect!\n\nCorrect answer: {correct_answer}"
        )

    explanation = explain_answer(
        q,
        a,
        b,
        c,
        d,
        correct_answer,
        answer
    )

    await update.message.reply_text(
        f"🤖 AI Explanation\n\n{explanation}"
    )

    if current_question >= total_questions(telegram_id):
        update_progress(
            telegram_id,
            current_question + 1,
            score
        )
        total = total_questions(telegram_id)
        percentage = (score / total) * 100

        if percentage >= 80:
            remark = "🌟 Excellent!"
        elif percentage >= 60:
            remark = "👏 Good Job!"
        elif percentage >= 40:
            remark = "📚 Keep Practicing!"
        else:
            remark = "💪 Don't Give Up!"

        await update.message.reply_text(
            f"""🎉 Quiz Completed!

        📊 Score: {score}/{total}
        📈 Percentage: {percentage:.1f}%

        {remark}
        """
        )
        return

    update_progress(
        telegram_id,
        current_question + 1,
        score
    )

    await take_quiz(update, context)
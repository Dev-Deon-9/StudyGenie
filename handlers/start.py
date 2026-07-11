from telegram import Update
from telegram.ext import ContextTypes

from keyboards.main_menu import main_menu
from database.database import user_exists, add_user

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    telegram_id = update.effective_user.id
    username = update.effective_user.username

    if not user_exists(telegram_id):
        add_user(telegram_id, name, username)
        message = (
            f"👋 *Welcome, {name}!*\n\n"
            "📚 Turn your study PDFs into AI-powered quizzes.\n\n"
            "Choose an option below to begin."
        )
    else:
        message = (
            f"👋 *Welcome back, {name}!*\n\n"
            "📚 Ready to continue learning.\n\n"
            "Choose an option below to begin."
        )
    await update.message.reply_text(
        message,
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

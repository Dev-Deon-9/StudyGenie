from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes

from database.admin_database import (
    get_total_users,
    get_total_pdfs,
    get_total_quizzes,
    get_total_flashcards,
)

ADMIN_ID = 7930223390


async def admin_panel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text(
            "❌ You are not authorized."
        )
        return

    total_users = get_total_users()
    total_pdfs = get_total_pdfs()
    total_quizzes = get_total_quizzes()
    total_flashcards = get_total_flashcards()

    keyboard = [
        [
            InlineKeyboardButton(
                "👥 Users",
                callback_data="admin_users"
            ),
            InlineKeyboardButton(
                "💬 Support",
                callback_data="admin_support"
            )
        ],
        [
            InlineKeyboardButton(
                "📢 Broadcast",
                callback_data="admin_broadcast"
            ),
            InlineKeyboardButton(
                "📥 Backup",
                callback_data="admin_backup"
            )
        ],
        [
            InlineKeyboardButton(
                "⭐ Premium",
                callback_data="admin_premium"
            ),
            InlineKeyboardButton(
                "🚫 Ban Users",
                callback_data="admin_ban"
            )
        ]
    ]

    await update.message.reply_text(
        f"""👑 StudyGenie Admin

📊 Dashboard

👥 Total Users: {total_users}
📄 PDFs Uploaded: {total_pdfs}
📝 Quizzes Generated: {total_quizzes}
🃏 Flashcards Generated: {total_flashcards}
⭐ Premium Users: 0
""",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


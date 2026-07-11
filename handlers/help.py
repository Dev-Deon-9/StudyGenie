from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)

from database.support_db import save_support_message
SUPPORT_MESSAGE = 1
waiting_for_support = set()

async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    keyboard = [
        [InlineKeyboardButton("📘 How to Use", callback_data="help_how")],
        [InlineKeyboardButton("💬 Contact Admin", callback_data="help_contact")],
        [InlineKeyboardButton("ℹ️ About StudyGenie", callback_data="help_about")],
        [InlineKeyboardButton("⬅ Back", callback_data="help_back")]
    ]

    await update.message.reply_text(
        """❓ StudyGenie Help

Welcome! How can we help you today?""",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def help_buttons(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    if query.data == "help_how":

        keyboard = [
            [
                InlineKeyboardButton(
                    "⬅ Back",
                    callback_data="help_menu"
                )
            ]
        ]

        await query.edit_message_text(
            """📘 How to Use StudyGenie

1️⃣ Upload a PDF using 📄 Upload PDF.

2️⃣ Generate quizzes from your uploaded PDFs.

3️⃣ Review key concepts using Flashcards.

4️⃣ Track your learning with Progress.

Need more help? Contact the admin from the Help menu.""",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "help_about":

        keyboard = [
            [
                InlineKeyboardButton(
                    "⬅ Back",
                    callback_data="help_menu"
                )
            ]
        ]

        await query.edit_message_text(
            """ℹ️ About StudyGenie

StudyGenie is your AI-powered study assistant.

❤️ Made to help students learn smarter, not harder.

Upload PDFs, generate quizzes, study with flashcards, and track your progress—all in one place.""",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "help_contact":

        waiting_for_support.add(query.from_user.id)

        await query.edit_message_text(
            """💬 Contact Admin

    Type your message below.

    It will be delivered to the admin."""
        )

    elif query.data == "help_menu":

        keyboard = [
            [
                InlineKeyboardButton(
                    "📘 How to Use",
                    callback_data="help_how"
                )
            ],
            [
                InlineKeyboardButton(
                    "💬 Contact Admin",
                    callback_data="help_contact"
                )
            ],
            [
                InlineKeyboardButton(
                    "ℹ️ About StudyGenie",
                    callback_data="help_about"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅ Back",
                    callback_data="help_back"
                )
            ]
        ]

        await query.edit_message_text(
            """❓ StudyGenie Help

Welcome! How can we help you today?""",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def receive_support_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user
    if user.id not in waiting_for_support:
        return

    save_support_message(
        user.id,
        user.first_name,
        user.username,
        update.message.text
    )
    waiting_for_support.remove(user.id)

    await update.message.reply_text(
        "✅ Your message has been sent to the admin."
    )

    return ConversationHandler.END
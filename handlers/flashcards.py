from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes

from database.flashcard_database import (
    connect_db,
    get_flashcard_progress,
    save_flashcard_progress,
)


async def show_flashcards(update: Update,
                          context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id

    progress = get_flashcard_progress(telegram_id)

    if progress:
        current_card, revealed = progress
    else:
        current_card = 1
        revealed = 0

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT card_number,
                          topic,
                          question
                   FROM flashcards
                   WHERE telegram_id = ?
                     AND card_number = ?
                   """, (telegram_id, current_card))

    card = cursor.fetchone()

    conn.close()

    if not card:
        await update.message.reply_text(
            "❌ You don't have any flashcards yet.\n\nUpload a PDF first."
        )
        return

    number, topic, question = card

    keyboard = [
        [
            InlineKeyboardButton(
                "🔓 Uncover Answer",
                callback_data=f"reveal_{number}"
            )
        ]
    ]

    await update.message.reply_text(
        f"""🃏 Flashcard {number}

    📚 Topic:
    {topic}

    ❓ {question}

    📖 Answer

    ████████████████████████
    ████████████████████████
    ████████████████████████

    👇 Tap below to uncover.
    """,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
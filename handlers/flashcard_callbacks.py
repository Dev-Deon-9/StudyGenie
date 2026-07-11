from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from database.flashcard_database import connect_db, save_flashcard_progress


async def reveal_answer(update: Update,
                        context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    number = int(query.data.split("_")[1])

    telegram_id = query.from_user.id

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT topic,
               question,
               answer
        FROM flashcards
        WHERE telegram_id = ?
        AND card_number = ?
        """,
        (
            telegram_id,
            number
        )
    )

    card = cursor.fetchone()

    conn.close()

    if not card:
        return

    topic, question, answer = card

    keyboard = [
        [
            InlineKeyboardButton(
                "⬅️ Previous",
                callback_data=f"previous_{number}"
            ),
            InlineKeyboardButton(
                "➡️ Next",
                callback_data=f"next_{number}"
            )
        ]
    ]

    await query.edit_message_text(
        f"""🃏 Flashcard {number}

📚 Topic:
{topic}

❓ {question}

📖 Answer

{answer}
""",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
async def next_card(update: Update,
                    context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    current = int(query.data.split("_")[1])
    next_number = current + 1

    telegram_id = query.from_user.id
    save_flashcard_progress(
        telegram_id,
        next_number,
        0
    )


    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT topic,
               question
        FROM flashcards
        WHERE telegram_id = ?
        AND card_number = ?
        """,
        (
            telegram_id,
            next_number
        )
    )

    card = cursor.fetchone()

    conn.close()

    if not card:
        await query.answer(
            "🎉 You've reached the last flashcard!",
            show_alert=True
        )
        return

    topic, question = card

    keyboard = [
        [
            InlineKeyboardButton(
                "🔓 Uncover Answer",
                callback_data=f"reveal_{next_number}"
            )
        ]
    ]

    await query.edit_message_text(
        f"""🃏 Flashcard {next_number}

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
async def previous_card(update: Update,
                        context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    current = int(query.data.split("_")[1])
    previous_number = current - 1
    telegram_id = query.from_user.id
    save_flashcard_progress(
        telegram_id,
        previous_number,
        0
    )

    if previous_number < 1:
        await query.answer(
            "📖 This is the first flashcard!",
            show_alert=True
        )
        return

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT topic,
               question
        FROM flashcards
        WHERE telegram_id = ?
        AND card_number = ?
        """,
        (
            telegram_id,
            previous_number
        )
    )

    card = cursor.fetchone()

    conn.close()

    if not card:
        return

    topic, question = card

    keyboard = [
        [
            InlineKeyboardButton(
                "🔓 Uncover Answer",
                callback_data=f"reveal_{previous_number}"
            )
        ]
    ]

    await query.edit_message_text(
        f"""🃏 Flashcard {previous_number}

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
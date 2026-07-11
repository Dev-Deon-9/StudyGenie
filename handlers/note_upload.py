from telegram import Update
from telegram.ext import ContextTypes
import os
import uuid

from ai.vision import read_note
from database.note_database import save_note

from ai.quiz_generator import generate_quiz

from database.quiz_database import (
    save_quiz,
    delete_old_quiz,
    start_progress,
)

async def ask_for_note(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "📸 Please upload a clear picture of your handwritten or printed study note."
    )


async def handle_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles uploaded study note images.
    """

    if not update.message.photo:
        await update.message.reply_text(
            "❌ Please upload a clear picture of your study note."
        )
        return

    await update.message.reply_text(
        "📖 Reading your note...\n\nThis may take a few seconds."
    )

    # Create temp folder
    os.makedirs("temp", exist_ok=True)

    # Create unique filename
    filename = f"{uuid.uuid4()}.jpg"
    image_path = os.path.join("temp", filename)

    try:
        # Get highest quality image
        photo = update.message.photo[-1]

        telegram_file = await photo.get_file()

        # Download image
        await telegram_file.download_to_drive(image_path)

        # Read note using Groq Vision
        note_text = read_note(image_path)
        save_note(
            update.effective_user.id,
            note_text
        )
        questions = generate_quiz(note_text)[:10]

        print(f"Generated {len(questions)} questions")

        delete_old_quiz(update.effective_user.id)

        start_progress(update.effective_user.id)

        for index, q in enumerate(questions, start=1):
            save_quiz(
                update.effective_user.id,
                index,
                q["question"],
                q["option_a"],
                q["option_b"],
                q["option_c"],
                q["option_d"],
                q["correct_answer"]
            )


        print("===== NOTE TEXT =====")
        print(note_text)
        print("=====================")

        await update.message.reply_text(
            "✅ Note uploaded successfully!\n\n📝 Your 10-question quiz is ready!"
        )

    except Exception as e:

        print(e)

        await update.message.reply_text(
            "❌ Failed to read your note."
        )

    finally:

        # Delete temporary image
        if os.path.exists(image_path):
            os.remove(image_path)
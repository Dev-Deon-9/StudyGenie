from telegram import Update
from telegram.ext import ContextTypes

ADMIN_ID = 7930223390

async def send_admin_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if update.effective_user.id != ADMIN_ID:
        return

    if "message_user" not in context.user_data:
        return

    telegram_id = context.user_data["message_user"]

    text = update.message.text

    try:
        await context.bot.send_message(
            chat_id=telegram_id,
            text=f"""📩 Message from StudyGenie Admin

{text}"""
        )

        await update.message.reply_text(
            "✅ Message sent successfully."
        )

    except Exception:
        await update.message.reply_text(
            "❌ Failed to send message."
        )

    del context.user_data["message_user"]
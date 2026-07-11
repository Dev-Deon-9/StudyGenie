from telegram import Update
from telegram.ext import ContextTypes


async def reply_user(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) < 2:
        await update.message.reply_text(
            "Usage:\n/reply <telegram_id> <message>"
        )
        return

    try:
        user_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text(
            "Invalid Telegram ID."
        )
        return

    message = " ".join(context.args[1:])

    try:
        await context.bot.send_message(
            chat_id=user_id,
            text=f"📩 Reply from StudyGenie Admin\n\n{message}"
        )

        await update.message.reply_text(
            "✅ Reply sent successfully."
        )

    except Exception as e:
        await update.message.reply_text(
            f"❌ Failed to send reply.\n\n{e}"
        )
from telegram.ext import (Application,
CommandHandler, MessageHandler, filters)
from handlers.pdf_upload import receive_pdf
from handlers.quiz import take_quiz
from handlers.answer import check_answer
from handlers.retake import retake_quiz
from handlers.flashcards import show_flashcards
from handlers.progress import show_progress
from handlers.admin import admin_panel
from handlers.admin_callbacks import admin_buttons
from handlers.admin_message import send_admin_message
from handlers.reply import reply_user
from handlers.help import (
    help_command,
    help_buttons,
    receive_support_message,
    SUPPORT_MESSAGE,
)
from database.support_db import create_support_table
from telegram.ext import CallbackQueryHandler
from handlers.flashcard_callbacks import (
    reveal_answer,
    next_card,
    previous_card,
)

from config import BOT_TOKEN
from handlers.start import start
from handlers.pdf_upload import ask_for_pdf
from database.database import create_tables
from database.pdf_database import create_pdf_table
from database.flashcard_database import (
    create_flashcard_table,
    create_flashcard_progress_table,
)

from handlers.note_upload import (
    ask_for_note,
    handle_note
)
from database.note_database import create_note_table

from database.quiz_database import (
    create_quiz_table,
    create_progress_table
)


app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(
    CommandHandler(
        "admin",
        admin_panel
    )
)

app.add_handler(
    CommandHandler(
        "help",
        help_command
    )
)



app.add_handler(
    MessageHandler(
        filters.TEXT & filters.Regex("^📄 Upload PDF$"),
        ask_for_pdf
    )
)
app.add_handler(
    MessageHandler(
        filters.TEXT & filters.Regex("^🖼️ Upload Notes$"),
        ask_for_note
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT & filters.Regex("^📝 Take Quiz$"),
        take_quiz
    )
)
app.add_handler(
    MessageHandler(
        filters.TEXT & filters.Regex("^🔄 Retake Quiz$"),
        retake_quiz
    )
)
app.add_handler(
    MessageHandler(
        filters.TEXT & filters.Regex("^🃏 Flashcards$"),
        show_flashcards
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT & filters.Regex("^📊 Progress$"),
        show_progress
    )
)

app.add_handler(
    MessageHandler(
        filters.Document.PDF,
        receive_pdf
    )
)


app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(
        filters.TEXT & filters.Regex("^[AaBbCcDd]$"),
        check_answer
    )
)

app.add_handler(
    CallbackQueryHandler(
        reveal_answer,
        pattern="^reveal_"
    )
)
app.add_handler(
    CallbackQueryHandler(
        next_card,
        pattern="^next_"
    )
)

app.add_handler(
    CallbackQueryHandler(
        previous_card,
        pattern="^previous_"
    )
)
app.add_handler(
    CallbackQueryHandler(
        admin_buttons,
        pattern="^(admin_|user_|premium_|ban_|files_|message_)"
    )
)

app.add_handler(
    CallbackQueryHandler(
        help_buttons,
        pattern="^help_"
    )
)
app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        receive_support_message
    )
)
app.add_handler(
    MessageHandler(
        filters.PHOTO,
        handle_note
    )
)

app.add_handler(
    CommandHandler(
        "reply",
        reply_user
    )
)
create_tables()
create_pdf_table()
create_progress_table()
create_flashcard_table()
create_quiz_table()
create_flashcard_progress_table()
create_support_table()
create_note_table()
from database.database import list_tables

list_tables()

print("🤖 StudyGenie is running...")

app.run_polling()
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import ContextTypes
from database.admin_database import (
    get_all_users,
    get_user,
    toggle_premium,
    toggle_ban,
    get_user_files,
)
from database.support_db import get_support_messages

async def admin_buttons(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    if query.data == "admin_users":

        users = get_all_users()

        if not users:
            await query.edit_message_text(
                "❌ No registered users."
            )
            return

        keyboard = []

        for telegram_id, first_name, username in users:

            if username:
                text = f"👤 {first_name} (@{username})"
            else:
                text = f"👤 {first_name}"

            keyboard.append([
                InlineKeyboardButton(
                    text,
                    callback_data=f"user_{telegram_id}"
                )
            ])

        keyboard.append([
            InlineKeyboardButton(
                "⬅ Back",
                callback_data="admin_back"
            )
        ])

        await query.edit_message_text(
            "👥 Registered Users",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif query.data.startswith("user_"):

        telegram_id = int(query.data.split("_")[1])

        user = get_user(telegram_id)

        (
            telegram_id,
            first_name,
            username,
            joined_at,
            pdfs_uploaded,
            quizzes_taken,
            premium,
            banned,
        ) = user

        premium_status = "Yes ✅" if premium else "No ❌"
        ban_button = (
            "✅ Unban User"
            if banned
            else
            "🚫 Ban User"
        )

        keyboard = [
            [
                InlineKeyboardButton(
                    "📂 View Files",
                    callback_data=f"files_{telegram_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    "💬 Message",
                    callback_data=f"message_{telegram_id}"
                ),
                InlineKeyboardButton(
                    "⭐ Premium",
                    callback_data=f"premium_{telegram_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    ban_button,
                    callback_data=f"ban_{telegram_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅ Back",
                    callback_data="admin_users"
                )
            ]
        ]

        await query.edit_message_text(
            f"""👤 User Profile

    🆔 {telegram_id}

    👤 {first_name}

    📛 @{username if username else 'No Username'}

    📅 Joined:
    {joined_at}

    📄 PDFs Uploaded: {pdfs_uploaded}
    📝 Quizzes Taken: {quizzes_taken}

    ⭐ Premium: {premium_status}
    """,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif query.data.startswith("premium_"):

        telegram_id = int(query.data.split("_")[1])

        new_status = toggle_premium(telegram_id)

        user = get_user(telegram_id)

        (
            telegram_id,
            first_name,
            username,
            joined_at,
            pdfs_uploaded,
            quizzes_taken,
            premium
        ) = user

        premium_status = "Yes ✅" if premium else "No ❌"

        keyboard = [
            [
                InlineKeyboardButton(
                    "📂 View Files",
                    callback_data=f"files_{telegram_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    "💬 Message",
                    callback_data=f"message_{telegram_id}"
                ),
                InlineKeyboardButton(
                    "⭐ Premium",
                    callback_data=f"premium_{telegram_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    "🚫 Ban",
                    callback_data=f"ban_{telegram_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅ Back",
                    callback_data="admin_users"
                )
            ]
        ]

        await query.edit_message_text(
            f"""👤 User Profile

    🆔 {telegram_id}

    👤 {first_name}

    📛 @{username if username else 'No Username'}

    📅 Joined:
    {joined_at}

    📄 PDFs Uploaded: {pdfs_uploaded}
    📝 Quizzes Taken: {quizzes_taken}

    ⭐ Premium: {premium_status}
    """,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )



    elif query.data.startswith("ban_"):

        telegram_id = int(query.data.split("_")[1])

        toggle_ban(telegram_id)

        user = get_user(telegram_id)

        (
            telegram_id,
            first_name,
            username,
            joined_at,
            pdfs_uploaded,
            quizzes_taken,
            premium,
            banned
        ) = user

        premium_status = "Yes ✅" if premium else "No ❌"

        ban_button = (
            "✅ Unban User"
            if banned
            else
            "🚫 Ban User"
        )

        keyboard = [
            [
                InlineKeyboardButton(
                    "📂 View Files",
                    callback_data=f"files_{telegram_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    "💬 Message",
                    callback_data=f"message_{telegram_id}"
                ),
                InlineKeyboardButton(
                    "⭐ Premium",
                    callback_data=f"premium_{telegram_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    ban_button,
                    callback_data=f"ban_{telegram_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅ Back",
                    callback_data="admin_users"
                )
            ]
        ]

        await query.edit_message_text(
            f"""👤 User Profile

    🆔 {telegram_id}

    👤 {first_name}

    📛 @{username if username else 'No Username'}

    📅 Joined:
    {joined_at}

    📄 PDFs Uploaded: {pdfs_uploaded}
    📝 Quizzes Taken: {quizzes_taken}

    ⭐ Premium: {premium_status}
    🚫 Banned: {"Yes ✅" if banned else "No ❌"}
    """,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data.startswith("files_"):

        telegram_id = int(query.data.split("_")[1])

        user = get_user(telegram_id)
        files = get_user_files(telegram_id)

        first_name = user[1]

        if not files:
            text = f"""📂 Uploaded Files

    👤 {first_name}

    No PDFs uploaded yet."""
        else:
            text = f"📂 Uploaded Files\n\n👤 {first_name}\n\n"

            for i, (file_name, uploaded_at) in enumerate(files, start=1):
                text += (
                    f"{i}. 📄 {file_name}\n"
                    f"🕒 {uploaded_at}\n\n"
                )

        keyboard = [
            [
                InlineKeyboardButton(
                    "⬅ Back",
                    callback_data=f"user_{telegram_id}"
                )
            ]
        ]

        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data.startswith("message_"):

        telegram_id = int(query.data.split("_")[1])

        context.user_data["message_user"] = telegram_id

        await query.message.reply_text(
            "💬 Send your message.\n\nType anything below.\n\n/cancel to cancel."
        )

    elif query.data == "admin_support":

        messages = get_support_messages()

        if not messages:
            await query.edit_message_text(
                "📭 No support messages yet."
            )
            return

        text = "💬 Support Inbox\n\n"

        for msg in messages:
            text += (
                f"👤 {msg[2]}\n"
                f"🆔 {msg[1]}\n"
                f"📄 {msg[4]}\n\n"
            )

        await query.edit_message_text(text)
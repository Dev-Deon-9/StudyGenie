import sqlite3


def create_support_table():
    DB_NAME = "data/studygenie.db"

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS support_messages (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            telegram_id INTEGER,

            first_name TEXT,

            username TEXT,

            message TEXT,

            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_support_message(
    telegram_id,
    first_name,
    username,
    message
):
    def get_support_messages():
        conn = sqlite3.connect("data/studygenie.db")
        cursor = conn.cursor()

        cursor.execute("""
                       SELECT id, first_name, username, message, created_at
                       FROM support_messages
                       ORDER BY id DESC
                       """)

        messages = cursor.fetchall()

        conn.close()

        return messages

    conn = sqlite3.connect("data/studygenie.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO support_messages (
            telegram_id,
            first_name,
            username,
            message
        )
        VALUES (?, ?, ?, ?)
    """, (
        telegram_id,
        first_name,
        username,
        message
    ))

    conn.commit()
    conn.close()


def get_support_users():

    conn = sqlite3.connect("studygenie.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT
            telegram_id,
            first_name,
            username
        FROM support_messages
        ORDER BY id DESC
    """)

    users = cursor.fetchall()

    conn.close()

    return users

def get_support_messages():
    conn = sqlite3.connect("data/studygenie.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, telegram_id, first_name, username, message
        FROM support_messages
        ORDER BY id DESC
    """)

    messages = cursor.fetchall()
    conn.close()

    return messages
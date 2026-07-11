import sqlite3
from config import DB_NAME


def create_note_table():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        telegram_id INTEGER,

        note_text TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()
    conn.close()


def save_note(telegram_id, note_text):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO notes
        (telegram_id, note_text)

        VALUES (?, ?)
        """,
        (telegram_id, note_text)
    )

    conn.commit()
    conn.close()
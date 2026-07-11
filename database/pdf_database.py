from database.database import connect_db

def create_pdf_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pdfs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            file_name TEXT,
            file_path TEXT,
            uploaded_at TEXT
        )
    """)

    conn.commit()
    conn.close()

from datetime import datetime


def save_pdf(telegram_id, file_name, file_path):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO pdfs (
            telegram_id,
            file_name,
            file_path,
            uploaded_at
        )
        VALUES (?, ?, ?, ?)
    """, (
        telegram_id,
        file_name,
        file_path,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()
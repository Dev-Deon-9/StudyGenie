import sqlite3
import os
from datetime import datetime

DB_NAME = "data/studygenie.db"


def connect_db():
    os.makedirs("data", exist_ok=True)   # Create the data folder if it doesn't exist

    print("Database path:", os.path.abspath(DB_NAME))

    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            first_name TEXT,
            username TEXT,
            joined_at TEXT,
            pdfs_uploaded INTEGER DEFAULT 0,
            quizzes_taken INTEGER DEFAULT 0,
            total_score INTEGER DEFAULT 0,
            premium INTEGER DEFAULT 0
        )
    """)
    try:
        cursor.execute("""
                       ALTER TABLE users
                           ADD COLUMN banned INTEGER DEFAULT 0
                       """)
    except:
        pass

    try:
        cursor.execute("""
                       ALTER TABLE users
                           ADD COLUMN banned INTEGER DEFAULT 0
                       """)
    except:
        pass
    conn.commit()
    conn.close()


def user_exists(telegram_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE telegram_id = ?",
        (telegram_id,)
    )

    user = cursor.fetchone()

    conn.close()

    return user


def add_user(telegram_id, first_name, username):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (
            telegram_id,
            first_name,
            username,
            joined_at
        )
        VALUES (?, ?, ?, ?)
    """, (
        telegram_id,
        first_name,
        username,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def list_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
    """)

    print("📋 Tables:", cursor.fetchall())

    conn.close()

def add_pdf_upload(telegram_id):
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
                       UPDATE users
                       SET pdfs_uploaded = pdfs_uploaded + 1
                       WHERE telegram_id = ?
                       """, (telegram_id,))

        conn.commit()
        conn.close()

def add_note_upload(telegram_id):
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
                       UPDATE users
                       SET notes_uploaded = notes_uploaded + 1
                       WHERE telegram_id = ?
                       """, (telegram_id,))

        conn.commit()
        conn.close()

def add_correct_answer(telegram_id):
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
                       UPDATE users
                       SET total_correct = total_correct + 1
                       WHERE telegram_id = ?
                       """, (telegram_id,))

        conn.commit()
        conn.close()

def add_wrong_answer(telegram_id):
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
                       UPDATE users
                       SET total_wrong = total_wrong + 1
                       WHERE telegram_id = ?
                       """, (telegram_id,))

        conn.commit()
        conn.close()

def add_quiz_taken(telegram_id):
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
                       UPDATE users
                       SET quizzes_taken = quizzes_taken + 1
                       WHERE telegram_id = ?
                       """, (telegram_id,))

        conn.commit()
        conn.close()

def get_profile(telegram_id):
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
                       SELECT first_name,
                              joined_at,
                              pdfs_uploaded,
                              notes_uploaded,
                              quizzes_taken,
                              total_correct,
                              total_wrong
                       FROM users
                       WHERE telegram_id = ?
                       """, (telegram_id,))

        profile = cursor.fetchone()

        conn.close()

        return profile
import sqlite3

DB_NAME = "data/studygenie.db"


def connect_db():
    return sqlite3.connect(DB_NAME)


def create_quiz_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quizzes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            question_number INTEGER,
            question TEXT,
            option_a TEXT,
            option_b TEXT,
            option_c TEXT,
            option_d TEXT,
            correct_answer TEXT
        )
    """)

    conn.commit()
    conn.close()

def create_progress_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_progress (
            telegram_id INTEGER PRIMARY KEY,
            current_question INTEGER DEFAULT 1,
            score INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()

def delete_old_quiz(telegram_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM quizzes WHERE telegram_id = ?",
        (telegram_id,)
    )

    conn.commit()
    conn.close()

def start_progress(telegram_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO quiz_progress
        (telegram_id, current_question, score)
        VALUES (?, 1, 0)
        """,
        (telegram_id,)
    )

    conn.commit()
    conn.close()


def get_progress(telegram_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT current_question, score
        FROM quiz_progress
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    progress = cursor.fetchone()

    conn.close()

    return progress

def get_question(telegram_id, question_number):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT question,
               option_a,
               option_b,
               option_c,
               option_d,
               correct_answer
        FROM quizzes
        WHERE telegram_id = ?
        AND question_number = ?
    """, (telegram_id, question_number))

    question = cursor.fetchone()

    conn.close()

    return question

def total_questions(telegram_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM quizzes
        WHERE telegram_id = ?
    """, (telegram_id,))

    count = cursor.fetchone()[0]

    conn.close()

    return count

def update_progress(telegram_id, question, score):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE quiz_progress
        SET current_question = ?, score = ?
        WHERE telegram_id = ?
        """,
        (question, score, telegram_id)
    )

    conn.commit()
    conn.close()

def save_quiz(
    telegram_id,
    question_number,
    question,
    option_a,
    option_b,
    option_c,
    option_d,
    correct_answer
):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO quizzes (
            telegram_id,
            question_number,
            question,
            option_a,
            option_b,
            option_c,
            option_d,
            correct_answer
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        telegram_id,
        question_number,
        question,
        option_a,
        option_b,
        option_c,
        option_d,
        correct_answer
    ))

    conn.commit()
    conn.close()
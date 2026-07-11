from database.database import connect_db


def create_flashcard_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            card_number INTEGER,
            topic TEXT,
            question TEXT,
            answer TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("✅ flashcards table created")
def create_flashcard_progress_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS flashcard_progress (
            telegram_id INTEGER PRIMARY KEY,
            current_card INTEGER,
            revealed INTEGER
        )
    """)

    conn.commit()
    conn.close()
def save_flashcard_progress(
    telegram_id,
    current_card,
    revealed
):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO flashcard_progress
        (
            telegram_id,
            current_card,
            revealed
        )
        VALUES (?, ?, ?)
    """, (
        telegram_id,
        current_card,
        revealed
    ))

    conn.commit()
    conn.close()
def get_flashcard_progress(telegram_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT current_card, revealed
        FROM flashcard_progress
        WHERE telegram_id = ?
    """, (telegram_id,))

    progress = cursor.fetchone()

    conn.close()

    return progress
def reset_flashcard_progress(telegram_id):
    save_flashcard_progress(
        telegram_id,
        1,
        0
    )




# 👇 PASTE THEM HERE


def delete_old_flashcards(telegram_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM flashcards
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    conn.commit()
    conn.close()


def save_flashcard(
    telegram_id,
    card_number,
    topic,
    question,
    answer
):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO flashcards(
            telegram_id,
            card_number,
            topic,
            question,
            answer
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            telegram_id,
            card_number,
            topic,
            question,
            answer
        )
    )

    conn.commit()
    conn.close()
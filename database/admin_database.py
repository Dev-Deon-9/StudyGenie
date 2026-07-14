from database.database import connect_db


def get_total_users():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM users
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_total_pdfs():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM pdfs
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_total_quizzes():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM quizzes
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_all_users():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            telegram_id,
            first_name,
            username
        FROM users
        ORDER BY first_name
    """)

    users = cursor.fetchall()

    conn.close()

    return users


def get_user(telegram_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            telegram_id,
            first_name,
            username,
            joined_at,
            pdfs_uploaded,
            quizzes_taken,
            premium,
            banned
        FROM users
        WHERE telegram_id = ?
    """, (telegram_id,))

    user = cursor.fetchone()

    conn.close()

    return user

def toggle_premium(telegram_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT premium
        FROM users
        WHERE telegram_id = ?
    """, (telegram_id,))

    current = cursor.fetchone()[0]

    new_value = 0 if current else 1

    cursor.execute("""
        UPDATE users
        SET premium = ?
        WHERE telegram_id = ?
    """, (new_value, telegram_id))

    conn.commit()
    conn.close()

    return new_value

def toggle_ban(telegram_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT banned
        FROM users
        WHERE telegram_id = ?
    """, (telegram_id,))

    current = cursor.fetchone()[0]

    new_value = 0 if current else 1

    cursor.execute("""
        UPDATE users
        SET banned = ?
        WHERE telegram_id = ?
    """, (new_value, telegram_id))

    conn.commit()
    conn.close()

    return new_value


def is_banned(telegram_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT banned
        FROM users
        WHERE telegram_id = ?
    """, (telegram_id,))

    banned = cursor.fetchone()[0]

    conn.close()

    return banned


def get_user_files(telegram_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            file_name,
            uploaded_at
        FROM pdfs
        WHERE telegram_id = ?
        ORDER BY uploaded_at DESC
    """, (telegram_id,))

    files = cursor.fetchall()

    conn.close()

    return files
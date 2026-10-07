import sqlite3
import os
import hashlib
import secrets


DATABASE_PATH = "database/encryption.db"


def get_connection():

    os.makedirs("database", exist_ok=True)

    return sqlite3.connect(DATABASE_PATH)


def create_users_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def hash_password(password, salt=None):

    if salt is None:
        salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        600000
    )

    return password_hash.hex(), salt


def create_user(username, password):

    password_hash, salt = hash_password(password)

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO users
            (username, password_hash, salt)
            VALUES (?, ?, ?)
        """, (
            username,
            password_hash,
            salt
        ))

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


def verify_user(username, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT password_hash, salt
        FROM users
        WHERE username = ?
    """, (username,))

    user = cursor.fetchone()

    conn.close()

    if not user:

        return False

    stored_hash, salt = user

    password_hash, _ = hash_password(
        password,
        salt
    )

    return secrets.compare_digest(
        stored_hash,
        password_hash
    )

def change_password(username, new_password):

    password_hash, salt = hash_password(new_password)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET password_hash = ?, salt = ?
        WHERE username = ?
    """, (
        password_hash,
        salt,
        username
    ))

    updated = cursor.rowcount > 0

    conn.commit()
    conn.close()

    return updated
def create_default_admin():

    username = os.environ.get("ADMIN_USERNAME")
    password = os.environ.get("ADMIN_PASSWORD")

    if not username or not password:
        return False

    create_users_table()

    password_hash, salt = hash_password(password)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM users
        WHERE username = ?
    """, (username,))

    existing_user = cursor.fetchone()

    if existing_user:

        cursor.execute("""
            UPDATE users
            SET password_hash = ?, salt = ?
            WHERE username = ?
        """, (
            password_hash,
            salt,
            username
        ))

    else:

        cursor.execute("""
            INSERT INTO users
            (username, password_hash, salt)
            VALUES (?, ?, ?)
        """, (
            username,
            password_hash,
            salt
        ))

    conn.commit()
    conn.close()

    return True
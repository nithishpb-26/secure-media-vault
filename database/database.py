
import sqlite3
import os


# ==============================
# DATABASE CONFIGURATION
# ==============================

DATABASE_PATH = "database/encryption.db"


# ==============================
# DATABASE CONNECTION
# ==============================

def get_connection():

    os.makedirs("database", exist_ok=True)

    return sqlite3.connect(DATABASE_PATH)


# ==============================
# CREATE DATABASE
# ==============================

def create_database():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS encryption_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            filename TEXT NOT NULL,

            operation TEXT NOT NULL,

            status TEXT NOT NULL,

            file_size INTEGER,

            sha256 TEXT,

            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP

        )
    """)

    # Add SHA-256 column if database already existed
    try:

        cursor.execute("""
            ALTER TABLE encryption_history
            ADD COLUMN sha256 TEXT
        """)

    except sqlite3.OperationalError:

        pass

    conn.commit()

    conn.close()


# ==============================
# SAVE HISTORY
# ==============================

def save_history(
    filename,
    operation,
    status,
    file_size,
    sha256=None
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO encryption_history
        (
            filename,
            operation,
            status,
            file_size,
            sha256
        )

        VALUES (?, ?, ?, ?, ?)
    """, (
        filename,
        operation,
        status,
        file_size,
        sha256
    ))

    conn.commit()

    conn.close()


# ==============================
# GET HISTORY
# ==============================

def get_history():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            filename,
            operation,
            status,
            file_size,
            sha256,
            timestamp

        FROM encryption_history

        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    conn.close()

    return records


# ==============================
# GET STATISTICS
# ==============================

def get_statistics():

    conn = get_connection()

    cursor = conn.cursor()

    # Total operations
    cursor.execute("""
        SELECT COUNT(*)
        FROM encryption_history
    """)

    total = cursor.fetchone()[0]

    # Successful operations
    cursor.execute("""
        SELECT COUNT(*)
        FROM encryption_history
        WHERE status = 'SUCCESS'
    """)

    successful = cursor.fetchone()[0]

    # Failed operations
    cursor.execute("""
        SELECT COUNT(*)
        FROM encryption_history
        WHERE status = 'FAILED'
    """)

    failed = cursor.fetchone()[0]

    # Encryption operations
    cursor.execute("""
        SELECT COUNT(*)
        FROM encryption_history
        WHERE operation = 'ENCRYPT'
    """)

    encryptions = cursor.fetchone()[0]

    # Decryption operations
    cursor.execute("""
        SELECT COUNT(*)
        FROM encryption_history
        WHERE operation = 'DECRYPT'
    """)

    decryptions = cursor.fetchone()[0]

    conn.close()

    return {

        "total": total,

        "successful": successful,

        "failed": failed,

        "encryptions": encryptions,

        "decryptions": decryptions

    }


# ==============================
# CREATE SECURITY LOGS TABLE
# ==============================

def create_security_logs_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS security_logs (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT,

            action TEXT NOT NULL,

            status TEXT NOT NULL,

            ip_address TEXT,

            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP

        )
    """)

    conn.commit()

    conn.close()


# ==============================
# SAVE SECURITY LOG
# ==============================

def save_security_log(
    username,
    action,
    status,
    ip_address=None
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO security_logs
        (
            username,
            action,
            status,
            ip_address
        )

        VALUES (?, ?, ?, ?)
    """, (
        username,
        action,
        status,
        ip_address
    ))

    conn.commit()

    conn.close()


# ==============================
# GET SECURITY LOGS
# ==============================

def get_security_logs():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            username,
            action,
            status,
            ip_address,
            timestamp

        FROM security_logs

        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    conn.close()

    return records


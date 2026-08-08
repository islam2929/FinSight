import sqlite3
import os

DB_NAME = "data/finsight.db"


def get_connection():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_NAME)


def create_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            merchant TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            transaction_type TEXT NOT NULL,
            description TEXT
        )
    """) 

    conn.commit()
    conn.close()


def add_transaction(
    date,
    merchant,
    category,
    amount,
    transaction_type,
    description
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions
        (date, merchant, category, amount, transaction_type, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        date,
        merchant,
        category,
        amount,
        transaction_type,
        description
    ))

    conn.commit()
    conn.close()


def get_transactions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM transactions
        ORDER BY date DESC
    """)

    transactions = cursor.fetchall()

    conn.close()

    return transactions


def update_transaction(
    transaction_id,
    date,
    merchant,
    category,
    amount,
    transaction_type,
    description
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE transactions
        SET date = ?,
            merchant = ?,
            category = ?,
            amount = ?,
            transaction_type = ?,
            description = ?
        WHERE id = ?
    """, (
        date,
        merchant,
        category,
        amount,
        transaction_type,
        description,
        transaction_id
    ))

    conn.commit()
    conn.close()


def delete_transaction(transaction_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM transactions
        WHERE id = ?
    """, (transaction_id,))

    conn.commit()
    conn.close()
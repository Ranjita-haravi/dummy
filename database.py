import sqlite3

def get_connection():
    conn = sqlite3.connect("inventory.db")
    return conn

def setup_database():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            sku TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT,
            price REAL CHECK(price >= 0),
            stock INTEGER CHECK(stock >= 0)
        )
    """)
    conn.commit()
    conn.close()

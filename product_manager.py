import sqlite3
from database import get_connection
from datetime import datetime

LOG_FILE = "logs.txt"

def log_action(action):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {action}\n")

def add_product():
    sku = input("Enter SKU: ")
    name = input("Enter product name: ")
    category = input("Enter category: ")
    price = float(input("Enter price: "))
    stock = int(input("Enter stock quantity: "))

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO products VALUES (?, ?, ?, ?, ?)", (sku, name, category, price, stock))
        conn.commit()
        print(f"Product '{name}' added successfully!")
    except sqlite3.IntegrityError:
        print("Error: SKU already.")
    finally:
        conn.close()

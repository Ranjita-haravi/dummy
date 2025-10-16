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
        print("Error: SKU already exists.")
    finally:
        conn.close()

def view_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No products found.")
    else:
        print("\nProduct Catalog:")
        print(f"{'SKU':<10}{'Name':<20}{'Category':<15}{'Price':<10}{'Stock':<10}")
        print("-"*65)
        for row in rows:
            print(f"{row[0]:<10}{row[1]:<20}{row[2]:<15}{row[3]:<10}{row[4]:<10}")

def edit_product():
    sku = input("Enter SKU of product to edit: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE sku = ?", (sku,))
    product = cursor.fetchone()

    if not product:
        print("Product not found.")
        conn.close()
        return

    print("Leave field blank to keep existing value.")
    new_name = input(f"New name ({product[1]}): ") or product[1]
    new_category = input(f"New category ({product[2]}): ") or product[2]
    new_price = input(f"New price ({product[3]}): ") or product[3]
    new_stock = input(f"New stock ({product[4]}): ") or product[4]

    cursor.execute("""
        UPDATE products 
        SET name=?, category=?, price=?, stock=? 
        WHERE sku=?
    """, (new_name, new_category, float(new_price), int(new_stock), sku))
    conn.commit()
    conn.close()
    print("Product updated successfully!")

def delete_product():
    sku = input("Enter SKU of product to delete: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM products WHERE sku = ?", (sku,))
    product = cursor.fetchone()

    if not product:
        print("Product not found.")
        conn.close()
        return

    confirm = input(f"Are you sure you want to delete '{product[0]}'? (y/n): ").lower()
    if confirm == 'y':
        cursor.execute("DELETE FROM products WHERE sku = ?", (sku,))
        conn.commit()
        log_action(f"Deleted product: {product[0]} (SKU: {sku})")
        print("Product deleted successfully.")
    else:
        print("Deletion canceled.")
    conn.close()

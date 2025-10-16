import os
import sqlite3
import pytest
from database import setup_database, get_connection
from product_manager import add_product

@pytest.fixture(scope="module", autouse=True)
def setup():
    # Setup fresh DB before tests
    if os.path.exists("inventory.db"):
        os.remove("inventory.db")
    setup_database()
    yield
    # Cleanup
    if os.path.exists("inventory.db"):
        os.remove("inventory.db")

def test_database_created():
    assert os.path.exists("inventory.db")

def test_add_product(monkeypatch):
    inputs = iter(["P001", "Keyboard", "Electronics", "1200", "10"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    add_product()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE sku='P001'")
    result = cursor.fetchone()
    conn.close()
    assert result is not None
    assert result[1] == "Keyboard"



import sqlite3
from database import get_connection
from models.product import Product
from datetime import datetime

class Movement:
    @staticmethod
    def move_product(name, to_department):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT department FROM products WHERE name = ?", (name,))
        result = cur.fetchone()

        if not result:
            print("❌ Product not found.")
            conn.close()
            return

        from_department = result[0]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cur.execute("""
            INSERT INTO movements (product_name, from_department, to_department, timestamp)
            VALUES (?, ?, ?, ?)
        """, (name, from_department, to_department, timestamp))

        conn.commit()
        conn.close()

        # Update department in products table
        Product.update_department(name, to_department)

    @staticmethod
    def get_history(product_name):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT from_department, to_department, timestamp
            FROM movements
            WHERE product_name = ?
            ORDER BY timestamp ASC
        """, (product_name,))
        history = cur.fetchall()
        conn.close()
        return history

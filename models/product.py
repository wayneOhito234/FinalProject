import sqlite3
from datetime import datetime
from database import get_connection


class Product:
    """Handles all product-related database operations."""

    @staticmethod
    def create_table():
        """Create products table if it doesn't exist."""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            client TEXT NOT NULL,
            completion_date TEXT NOT NULL,
            department_id INTEGER,
            status TEXT DEFAULT 'In Progress',
            FOREIGN KEY(department_id) REFERENCES departments(id)
        )
        """)
        conn.commit()
        conn.close()

    # ------------------------------------------------------
    @staticmethod
    def add_product(name, client, completion_date, department_id):
        """Add a new product to the database."""
        conn = get_connection()
        cur = conn.cursor()

        if not name or not client:
            print("⚠️ Product name and client are required.")
            conn.close()
            return False

        cur.execute("""
            INSERT INTO products (name, client, completion_date, department_id)
            VALUES (?, ?, ?, ?)
        """, (name, client, completion_date, department_id))

        # Log product creation
        cur.execute("""
            INSERT INTO product_movements (product_id, department_id, timestamp)
            VALUES ((SELECT MAX(id) FROM products), ?, ?)
        """, (department_id, datetime.now().isoformat()))

        conn.commit()
        conn.close()
        return True

    # ------------------------------------------------------
    @staticmethod
    def get_all_products():
        """Return all products with department and status."""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT p.id, p.name, p.client, p.completion_date, d.name, p.status
            FROM products p
            LEFT JOIN departments d ON p.department_id = d.id
            ORDER BY p.id
        """)
        rows = cur.fetchall()
        conn.close()
        return rows

    # ------------------------------------------------------
    @staticmethod
    def move_product(product_id, new_department_id):
        """Move product to next department and log movement."""
        conn = get_connection()
        cur = conn.cursor()

        # Update department
        cur.execute("""
            UPDATE products
            SET department_id = ?
            WHERE id = ?
        """, (new_department_id, product_id))

        # Log movement
        cur.execute("""
            INSERT INTO product_movements (product_id, department_id, timestamp)
            VALUES (?, ?, ?)
        """, (product_id, new_department_id, datetime.now().isoformat()))

        conn.commit()
        conn.close()

    # ------------------------------------------------------
    @staticmethod
    def delete_product(product_id):
        """Delete a product permanently."""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        conn.close()

    # ------------------------------------------------------
    @staticmethod
    def get_product_history(product_id):
        """Fetch a product's movement history."""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT d.name, pm.timestamp
            FROM product_movements pm
            LEFT JOIN departments d ON pm.department_id = d.id
            WHERE pm.product_id = ?
            ORDER BY pm.timestamp
        """, (product_id,))
        rows = cur.fetchall()
        conn.close()
        return rows

    # ------------------------------------------------------
    @staticmethod
    def mark_completed(product_id):
        """Mark a product as completed when it reaches Dispatch."""
        conn = get_connection()
        cur = conn.cursor()

        # Update product status
        cur.execute("""
            UPDATE products
            SET status = 'Completed'
            WHERE id = ?
        """, (product_id,))

        # Log completion (NULL department means finished)
        cur.execute("""
            INSERT INTO product_movements (product_id, department_id, timestamp)
            VALUES (?, NULL, ?)
        """, (product_id, datetime.now().isoformat()))

        conn.commit()
        conn.close()
        print("✅ Product marked as Completed.")

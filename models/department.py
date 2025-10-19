import sqlite3
from database import get_connection


class Department:
    @staticmethod
    def create_table():
        """Create departments table if not exists."""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            order_no INTEGER NOT NULL
        )
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def get_all_departments():
        """Return all departments ordered by order_no."""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, order_no FROM departments ORDER BY order_no")
        rows = cur.fetchall()
        conn.close()
        return rows

    @staticmethod
    def add_department(name, before_name):
        """Add a new department in a specific order."""
        conn = get_connection()
        cur = conn.cursor()

        # Get all existing departments
        cur.execute("SELECT id, name, order_no FROM departments ORDER BY order_no")
        departments = cur.fetchall()
        names = [d[1] for d in departments]

        if not departments:
            # If no departments exist yet
            cur.execute("INSERT INTO departments (name, order_no) VALUES (?, ?)", (name, 1))
            conn.commit()
            conn.close()
            return True

        # If 'before_name' is given and exists
        if before_name in names:
            position = names.index(before_name)
            # Shift order_no for departments that come after this position
            cur.execute("UPDATE departments SET order_no = order_no + 1 WHERE order_no >= ?", (position + 1,))
            cur.execute("INSERT INTO departments (name, order_no) VALUES (?, ?)", (name, position + 1))
        else:
            # Add at the end
            cur.execute("SELECT MAX(order_no) FROM departments")
            max_order = cur.fetchone()[0] or 0
            cur.execute("INSERT INTO departments (name, order_no) VALUES (?, ?)", (name, max_order + 1))

        conn.commit()
        conn.close()
        return True

    @staticmethod
    def delete_department(name):
        """Delete a department by name and reorder sequence."""
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT order_no FROM departments WHERE name = ?", (name,))
        result = cur.fetchone()
        if not result:
            conn.close()
            return False

        order_no = result[0]
        cur.execute("DELETE FROM departments WHERE name = ?", (name,))
        cur.execute("UPDATE departments SET order_no = order_no - 1 WHERE order_no > ?", (order_no,))
        conn.commit()
        conn.close()
        return True

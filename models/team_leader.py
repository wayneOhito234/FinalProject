import sqlite3
from database import get_connection


class TeamLeader:
    """Handles all operations related to Team Leaders in the manufacturing system."""

    @staticmethod
    def get_all_team_leaders():
        """Fetch all team leaders with their assigned departments."""
        conn = get_connection()
        cur = conn.cursor()

        # Ensure table exists before querying
        cur.execute("""
        CREATE TABLE IF NOT EXISTS team_leaders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            department_id INTEGER,
            FOREIGN KEY (department_id) REFERENCES departments(id)
        )
        """)

        cur.execute("""
            SELECT tl.id, tl.name, d.name AS department
            FROM team_leaders tl
            LEFT JOIN departments d ON tl.department_id = d.id
            ORDER BY tl.id ASC
        """)
        data = cur.fetchall()
        conn.close()
        return data

    @staticmethod
    def add_team_leader(name, department_id):
        """Add a new team leader to a department."""
        conn = get_connection()
        cur = conn.cursor()

        # Validate department existence
        cur.execute("SELECT id FROM departments WHERE id = ?", (department_id,))
        if not cur.fetchone():
            print("⚠️ Department not found.")
            conn.close()
            return False

        # Check for existing team leader with same name
        cur.execute("SELECT * FROM team_leaders WHERE name = ?", (name,))
        if cur.fetchone():
            print("⚠️ Team leader already exists.")
            conn.close()
            return False

        # Check if department already has a leader
        cur.execute("SELECT * FROM team_leaders WHERE department_id = ?", (department_id,))
        existing = cur.fetchone()
        if existing:
            print("⚠️ This department already has a team leader.")
            conn.close()
            return False

        # Insert new team leader
        cur.execute(
            "INSERT INTO team_leaders (name, department_id) VALUES (?, ?)",
            (name, department_id)
        )
        conn.commit()
        conn.close()
        print("✅ Team leader added successfully.")
        return True

    @staticmethod
    def delete_team_leader(name):
        """Delete a team leader by name."""
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM team_leaders WHERE name = ?", (name,))
        leader = cur.fetchone()
        if not leader:
            print("⚠️ Team leader not found.")
            conn.close()
            return False

        cur.execute("DELETE FROM team_leaders WHERE name = ?", (name,))
        conn.commit()
        conn.close()
        print("🗑️ Team leader deleted successfully.")
        return True

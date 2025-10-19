import sqlite3
import os

DB_NAME = "manufacturing.db"


def get_connection():
    """Establish and return a database connection."""
    return sqlite3.connect(DB_NAME)


def init_db():
    """Initialize or upgrade the database with all required tables."""
    conn = get_connection()
    cur = conn.cursor()

    # --- Departments Table ---
    cur.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            order_no INTEGER NOT NULL
        )
    """)

    # --- Team Leaders Table ---
    cur.execute("""
        CREATE TABLE IF NOT EXISTS team_leaders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    # ✅ Ensure 'department_id' column exists in team_leaders
    cur.execute("PRAGMA table_info(team_leaders)")
    columns = [col[1] for col in cur.fetchall()]
    if "department_id" not in columns:
        print("🧩 Adding missing 'department_id' column to team_leaders...")
        cur.execute("ALTER TABLE team_leaders ADD COLUMN department_id INTEGER")
        conn.commit()

    # --- Clients Table ---
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    # --- Products Table ---
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

    # --- Product Movements Table ---
    cur.execute("""
        CREATE TABLE IF NOT EXISTS product_movements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            department_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY(product_id) REFERENCES products(id),
            FOREIGN KEY(department_id) REFERENCES departments(id)
        )
    """)

    # ✅ Check if department_id is NOT NULL and fix it automatically
    cur.execute("PRAGMA table_info(product_movements)")
    columns = cur.fetchall()
    dept_nullable = True
    for col in columns:
        if col[1] == "department_id":
            dept_nullable = (col[3] == 0)  # 0 = NULL allowed, 1 = NOT NULL

    if not dept_nullable:
        print("🔧 Fixing 'product_movements' table to allow NULL for department_id...")

        # 1️⃣ Create new temp table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS product_movements_temp (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                department_id INTEGER,
                timestamp TEXT NOT NULL,
                FOREIGN KEY(product_id) REFERENCES products(id),
                FOREIGN KEY(department_id) REFERENCES departments(id)
            )
        """)

        # 2️⃣ Copy existing data
        cur.execute("""
            INSERT INTO product_movements_temp (product_id, department_id, timestamp)
            SELECT product_id, department_id, timestamp FROM product_movements
        """)

        # 3️⃣ Drop old table and rename new one
        cur.execute("DROP TABLE product_movements")
        cur.execute("ALTER TABLE product_movements_temp RENAME TO product_movements")
        print("✅ 'department_id' column in product_movements now allows NULL.")

    # --- Progress Table ---
    cur.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            progress INTEGER DEFAULT 0,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    """)

    # ✅ Insert default departments if none exist
    cur.execute("SELECT COUNT(*) FROM departments")
    if cur.fetchone()[0] == 0:
        default_departments = [
            ("Design", 1),
            ("Fabrication", 2),
            ("Panel Assembly", 3),
            ("Dispatch", 4)
        ]
        cur.executemany("INSERT INTO departments (name, order_no) VALUES (?, ?)", default_departments)
        print("🏢 Default departments added.")

    conn.commit()
    conn.close()
    print("✅ Database initialized and upgraded successfully.")

import os
import sqlite3
from database import init_db
from models.department import Department
from models.team_leader import TeamLeader
from models.product import Product
from models.movement import Movement


def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")


def menu():
    """Main interactive CLI menu"""
    init_db()
    while True:
        print("\n🏭 MANUFACTURING TRACKING SYSTEM")
        print("--------------------------------")
        print("1. Add Department")
        print("2. Add Team Leader")
        print("3. Add Product")
        print("4. Move Product")
        print("5. Delete Product")
        print("6. List All Products & Current Departments")
        print("7. View Product Movement History")
        print("8. View Client Summary")
        print("9. Delete Team Leader")
        print("10. Initialize Database")
        print("11. View Departments")
        print("12. Delete Department")
        print("0. Exit")

        choice = input("\nEnter your choice (0-12): ").strip()

        if choice == "1":
            add_department()
        elif choice == "2":
            add_team_leader()
        elif choice == "3":
            add_product()
        elif choice == "4":
            move_product()
        elif choice == "5":
            delete_product()
        elif choice == "6":
            list_products()
        elif choice == "7":
            view_movement_history()
        elif choice == "8":
            view_client_summary()
        elif choice == "9":
            delete_team_leader()
        elif choice == "10":
            init_db()
            print("✅ Database reinitialized successfully.")
        elif choice == "11":
            view_departments()
        elif choice == "12":
            delete_department()
        elif choice == "0":
            print("👋 Exiting system. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select between 0-12.")


# --------------------- DEPARTMENT -----------------------

def add_department():
    """Add a new department in sequence."""
    print("\n📋 Existing Departments:")
    departments = Department.get_all_departments()
    for d in departments:
        print(f" - {d[1]}")

    name = input("\nEnter new department name: ").strip()
    if not name.replace(" ", "").isalpha():
        print("⚠️ Department name must contain only letters and spaces.")
        return

    before_name = input("Where should this department come? (before which department name): ").strip()

    if Department.add_department(name, before_name):
        print(f"✅ Department '{name}' added successfully.")
    else:
        print("❌ Failed to add department.")


def view_departments():
    """Display all departments in order."""
    print("\n🏢 Departments (in order):")
    departments = Department.get_all_departments()
    for d in departments:
        print(f" {d[0]}. {d[1]}")


def delete_department():
    """Delete a department by name."""
    print("\n🏢 Departments:")
    departments = Department.get_all_departments()
    for d in departments:
        print(f" - {d[1]}")
    name = input("Enter department name to delete: ").strip()
    if Department.delete_department(name):
        print(f"✅ Department '{name}' deleted successfully.")
    else:
        print("❌ Department not found.")


# --------------------- TEAM LEADER -----------------------

def add_team_leader():
    """Add a new team leader to a department."""
    print("\n👨‍🔧 Existing Team Leaders:")
    leaders = TeamLeader.get_all_team_leaders()

    if leaders:
        for leader in leaders:
            print(f"   ID: {leader[0]} | Name: {leader[1]} | Department: {leader[2] or 'Unassigned'}")
    else:
        print("   No team leaders found.")

    # --- List available departments ---
    print("\n🏢 Available Departments:")
    departments = Department.get_all_departments()
    for dept in departments:
        print(f"   ID: {dept[0]} | Name: {dept[1]}")

    # --- Get inputs from user ---
    name = input("Enter team leader name: ").strip()
    department_id = input("Enter department ID to assign this leader: ").strip()

    if not department_id.isdigit():
        print("⚠️ Invalid department ID.")
        return

    # --- Add team leader ---
    if TeamLeader.add_team_leader(name, int(department_id)):
        print("✅ Team leader added successfully.")
    else:
        print("❌ Failed to add team leader.")


def delete_team_leader():
    """Delete a team leader."""
    print("\n👨‍🔧 Existing Team Leaders:")
    leaders = TeamLeader.get_all_team_leaders()
    if not leaders:
        print("   No team leaders found.")
        return

    for l in leaders:
        print(f" - {l[1]}")
    name = input("Enter team leader name to delete: ").strip()
    if TeamLeader.delete_team_leader(name):
        print(f"✅ Team Leader '{name}' deleted successfully.")
    else:
        print("❌ Team Leader not found.")


# --------------------- PRODUCT -----------------------

def add_product():
    """Add a new product."""
    print("\n📦 Existing Products:")
    products = Product.get_all_products()
    if not products:
        print("   No products found yet.")
    else:
        for p in products:
            print(f" - {p[1]} ({p[2]}) [{p[4] if p[4] else 'No department'}]")

    client = input("Enter client name: ").strip()
    name = input("Enter product name: ").strip()
    deadline = input("Enter completion timeline (e.g. 2025-12-31): ").strip()

    # Auto-start in Design department
    departments = Department.get_all_departments()
    first_department = departments[0][0] if departments else None

    if Product.add_product(name, client, deadline, first_department):
        print(f"✅ Product '{name}' added and started in the 'Design' department.")
    else:
        print("❌ Failed to add product.")


def move_product():
    """Move product through department flow."""
    products = Product.get_all_products()
    if not products:
        print("\n⚠️ No products found.")
        return

    print("\n📦 Products:")
    for p in products:
        print(f"{p[0]}. {p[1]} - {p[4]} (Status: {p[5]})")

    try:
        pid = int(input("Enter Product ID to move: "))
    except ValueError:
        print("❌ Invalid input.")
        return

    departments = Department.get_all_departments()
    current_dept = None
    for p in products:
        if p[0] == pid:
            current_dept = p[4]
            break

    if not current_dept:
        print("❌ Product not found.")
        return

    dept_names = [d[1] for d in departments]
    if current_dept == "Dispatch":
        print("✅ Product has reached Dispatch. Marking as Completed.")
        Product.mark_completed(pid)
        return

    next_index = dept_names.index(current_dept) + 1
    if next_index < len(dept_names):
        next_dept_id = departments[next_index][0]
        Product.move_product(pid, next_dept_id)
        print(f"➡️ Product moved to {dept_names[next_index]}")
    else:
        print("⚠️ Product already in the final department.")


def delete_product():
    """Delete a product."""
    products = Product.get_all_products()
    if not products:
        print("\n⚠️ No products found.")
        return

    for p in products:
        print(f"{p[0]}. {p[1]} - {p[2]}")

    try:
        pid = int(input("Enter Product ID to delete: "))
    except ValueError:
        print("❌ Invalid input.")
        return

    Product.delete_product(pid)
    print("✅ Product deleted successfully.")


def list_products():
    """List all products and their current departments."""
    products = Product.get_all_products()
    if not products:
        print("\n⚠️ No products found.")
        return
    print("\n📋 Products:")
    for p in products:
        print(f"{p[1]} ({p[2]}) - Department: {p[4]} | Status: {p[5]}")


def view_movement_history():
    """View a product’s movement history."""
    try:
        pid = int(input("Enter Product ID: "))
    except ValueError:
        print("❌ Invalid input.")
        return

    history = Product.get_product_history(pid)
    if not history:
        print("⚠️ No movement history found.")
        return
    print("\n📜 Movement History:")
    for h in history:
        print(f" - {h[0]} at {h[1]}")


def view_client_summary():
    """Show client summary."""
    conn = sqlite3.connect("manufacturing.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT client,
            COUNT(*) as total,
            SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) as completed,
            SUM(CASE WHEN status != 'Completed' THEN 1 ELSE 0 END) as pipeline
        FROM products
        GROUP BY client
    """)
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("\n⚠️ No client data available.")
        return

    print("\n👥 Client Summary:")
    for r in rows:
        print(f"{r[0]} → Total: {r[1]}, Completed: {r[2]}, Pipeline: {r[3]}")


# --------------------- RUN -----------------------

if __name__ == "__main__":
    menu()

#  Manufacturing Process Tracking System (CLI Version)
## Overview
The Manufacturing Process Tracking System is a Python-based command-line interface (CLI) application designed to manage and monitor the production flow of products through various departments in a manufacturing company.

It allows users to:

a) Add and organize Departments in a logical sequence
b) Register Team Leaders per department
c) Add, track, and move Products through the production pipeline
d) Record and view Movement History
e) Generate Client Summaries

Manage all records directly via a simple interactive CLI menu

## Features
🔹 Department Management
Add new departments in sequence
View all departments in their order of operation
Delete existing departments

🔹 Team Leader Management
Assign team leaders to specific departments
View all team leaders with their assigned departments
Delete team leaders when necessary

🔹 Product Management
Add new products with client and completion timelines
Automatically start products in the first department (e.g., Design)
Move products through the department chain
View product movement history
Delete products

🔹 Reports & Insights
View all products and their current departments
Generate client summary reports (total, completed, and ongoing products)

## Project Structure
FinalProject/
│
├── cli.py                     # Main interactive CLI application
├── database.py                # Handles DB connection and schema initialization
│
├── models/
│   ├── department.py          # Department model and logic
│   ├── team_leader.py         # Team leader model and logic
│   ├── product.py             # Product model and logic
│   ├── movement.py            # Product movement tracking
│
├── manufacturing.db           # SQLite database (auto-created)
└── README.md                  # Project documentation

## Installation and Setup
1. Clone the repository
```bash
git clone https://github.com/<wayneOhito234>/FinalProject.git
cd FinalProject
```
2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate   # On Windows → venv\Scripts\activate
```
3. Install dependecies
```bash
pip install -r requirements.txt  # (Optional if you add dependencies later)
```
4. Initialize the database
```bash
python -c "from database import init_db; init_db()"
```
5. Run the application
```bash
python cli.py
```
## Technologies Used
Python 3
SQLite3 for lightweight data storage
Object-Oriented Programming (OOP) design pattern

## Developer Notes
All database interactions are handled through database.py for consistency.
init_db() automatically creates all necessary tables if they don’t exist.
CLI is designed for easy expansion — you can add new models or menus seamlessly.

## Author
Wayne Ohito
Electrical & Electronics Engineering Student

## License

This project is open-source and available under the MIT License.






import sqlite3
from tabulate import tabulate

def test_database_connection(db_path):
    try:
        conn = sqlite3.connect(db_path)
        conn.execute('SELECT 1')
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error connecting to the database: {e}")
        return False

def print_users(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT * FROM Users')
    users_rows = c.fetchall()
    conn.close()

    if users_rows:
        headers = [desc[0] for desc in c.description]
        print("Users:")
        print(tabulate(users_rows, headers=headers, tablefmt='grid'))
    else:
        print("No users in the database.")

def print_tasks(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT * FROM tasks')
    tasks_rows = c.fetchall()
    conn.close()

    if tasks_rows:
        headers = [desc[0] for desc in c.description]
        print("Tasks:")
        print(tabulate(tasks_rows, headers=headers, tablefmt='grid'))
    else:
        print("No tasks in the database.")

def print_categories(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(f'SELECT * FROM categories')
    category_rows = c.fetchall()
    conn.close()

    if category_rows:
        headers = [desc[0] for desc in c.description]
        print("Categories:")
        print(tabulate(category_rows, headers=headers, tablefmt='grid'))
    else:
        print("No categories in the database.")

def print_subcategories(db_path, category_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        f'SELECT * FROM subcategories WHERE category_id = ?', (category_id,))
    subcategories_rows = c.fetchall()
    conn.close()

    if subcategories_rows:
        headers = [desc[0] for desc in c.description]
        print("Subcategories:")
        print(tabulate(subcategories_rows, headers=headers, tablefmt='grid'))
    else:
        print("No subcategories in the database.")

def print_logs(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT * FROM logs')
    logs_rows = c.fetchall()
    conn.close()

    if logs_rows:
        headers = [desc[0] for desc in c.description]
        print("Logs:")
        print(tabulate(logs_rows, headers=headers, tablefmt='grid'))
    else:
        print("No logs in the database.")

db_path = '/Users/alessandrazamora/butler/databases/butler_database.db'

if test_database_connection(db_path):
    print("Database connection is successful.")
    # Print the contents of the database
    print_users(db_path)
    print_tasks(db_path)
    print_categories(db_path)
    # Example: Print subcategories for a specific category (replace 1 with the actual category ID)
    print_subcategories(db_path, 1)
    print_logs(db_path)
else:
    print("Unable to connect to the database.")

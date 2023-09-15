import sqlite3
from tabulate import tabulate

def test_database_connection():
    try:
        # Update the filename here
        conn = sqlite3.connect('/Users/alessandrazamora/butler/databases/butler_database.db')
        conn.execute('SELECT 1')
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error connecting to the database: {e}")
        return False


def print_users():
    conn = sqlite3.connect('/Users/alessandrazamora/butler/databases/butler_database.db')  # Update the filename here
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


def print_tasks():
    conn = sqlite3.connect('/Users/alessandrazamora/butler/databases/butler_database.db')  # Update the filename here
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


def print_logs():
    conn = sqlite3.connect('/Users/alessandrazamora/butler/databases/butler_database.db')  # Update the filename here
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


if test_database_connection():
    print("Database connection is successful.")
    # Print the contents of the database
    print_users()
    print_tasks()
    print_logs()

else:
    print("Unable to connect to the database.")

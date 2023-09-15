import sqlite3
from unicodedata import category
from colorama import init, Fore, Style
from task_calculations import get_user_id, start_task
from expenses import start_expense_log

init(autoreset=True)


def connect_to_database():
    conn = sqlite3.connect(
        '/Users/alessandrazamora/butler/databases/butler_database.db')
    return conn


def close_connection(conn):
    conn.close()


def add_user():
    username = input("Enter username: ")
    conn = connect_to_database()
    c = conn.cursor()
    c.execute("INSERT INTO users (name) VALUES (?)", (username,))
    conn.commit()
    close_connection(conn)


def add_task():
    task_name = input("Enter task name: ")

    conn = connect_to_database()
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task_name) VALUES (?)", (task_name,))
    conn.commit()
    close_connection(conn)

# add categories
# Function to add subcategories

# Function to add a new category


def add_category():
    category_name = input("Enter category name: ")
    conn = connect_to_database()
    c = conn.cursor()

    # Insert the new category into the categories table
    c.execute("INSERT INTO categories (category_name) VALUES (?)",
              (category_name,))
    conn.commit()
    close_connection(conn)

    print(f"Category '{category_name}' added.")


def add_subcategory():
    conn = connect_to_database()
    c = conn.cursor()

    # Display existing categories
    c.execute("SELECT category_id, category_name FROM categories")
    categories = c.fetchall()

    if not categories:
        print(Fore.RED + "No categories exist. Please add a category first." + Fore.RESET)
        close_connection(conn)
        return

    print("Existing Categories:")
    for category_id, category_name in categories:
        print(f"{category_id}. {category_name}")

    # Ask the user to choose a category
    chosen_category_id = input(
        "Enter the category ID to add a subcategory to: ")

    # Check if the chosen_category_id is valid
    if not chosen_category_id.isdigit():
        print(Fore.RED + "Invalid category ID." + Fore.RESET)
        close_connection(conn)
        return

    chosen_category_id = int(chosen_category_id)

    # Check if the chosen_category_id exists in the categories table
    if chosen_category_id not in [category[0] for category in categories]:
        print(Fore.RED + "Category ID not found." + Fore.RESET)
        close_connection(conn)
        return

    subcategory_name = input(
        f"Enter subcategory name for category ID {chosen_category_id}: ")

    # Insert the subcategory into the subcategories table
    c.execute("INSERT INTO subcategories (subcategory_name, category_id) VALUES (?, ?)",
              (subcategory_name, chosen_category_id))
    conn.commit()

    print(
        f"Subcategory '{subcategory_name}' added to category ID {chosen_category_id}.")
    close_connection(conn)

def user_login():
    user_log = input(Fore.BLUE + "Enter username: " + Fore.RESET)
    conn = connect_to_database()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE name = ?', (user_log,))
    result = c.fetchone()
    if result:
        print(Fore.GREEN + f"Welcome, {user_log}!" + Fore.RESET)
        user_id = get_user_id(user_log)
        start_task(user_log, user_id)
    else:
        print(Fore.RED + "User not found. " + Fore.RESET + Fore.YELLOW +
              "Would you like to create a username?" + Fore.RESET)
        response = input(Fore.GREEN + 'Enter Y or N: ' + Fore.RESET)
        if response.upper() == 'Y':
            add_user(user_log)
        elif response.upper() == 'N':
            print(Fore.RED + 'Okay, operation canceled.' + Fore.RESET)
    conn.commit()
    close_connection(conn)


def add_expenses():
    username = input(Fore.MAGENTA + "Enter your username:" + Fore.RESET)
    user_id = get_user_id(username)
    start_expense_log(username, user_id)


def stats():
    print('here go the data visualization daily/weekly/monthly/yearly')
    print('Ask from when to when user would like to see stats')


def print_welcome():
    art = '''
          ──────▄▀▄─────▄▀▄
          ─────▄█░░▀▀▀▀▀░░█▄
          ─▄▄──█░░░░░░░░░░░█──▄▄
          █▄▄█─█░░▀░░┬░░▀░░█─█▄▄█
     _   _   _   _   _   _   _   _   _  
    / \ / \ / \ / \ / \ / \ / \ / \ / \ 
   ( F | a | i | r | S | h | a | r | e )
    \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ 
    '''
    print(Fore.MAGENTA + art + Fore.RESET)
    print(' ')
    print(Fore.BLUE + "Hello. How can I be of service today?" + Fore.RESET)


def main():
    print_welcome()
    while True:
        print(Fore.YELLOW + "1. Add new user" + Fore.RESET)
        print(Fore.GREEN + "2. Add new task (e.g Mopping floor)" + Fore.RESET)
        print(Fore.LIGHTBLUE_EX + "3. Add new category (e.g Housing)" + Fore.RESET)
        print(Fore.LIGHTYELLOW_EX + "4. Add new subcategory (e.g. Housing -> Rent)")
        print(Fore.RED + "5. Login task" + Fore.RESET)
        print(Fore.LIGHTMAGENTA_EX + "6. Login expenses" + Fore.RESET)
        print(Fore.MAGENTA + "7. View stats" + Fore.RESET)
        print(Fore.CYAN + "8. Exit" + Fore.RESET)

        choice = input(
            Fore.BLUE + "Enter your choice (1/2/3/4/5/6): " + Fore.RESET)

        if choice == '1':
            add_user()
            print(Fore.GREEN + "User added successfully!" + Fore.RESET)
        elif choice == '2':
            add_task()
            print(Fore.GREEN + "Task added successfully!" + Fore.RESET)
        elif choice == '3':
            add_category()
            print(Fore.GREEN + "Category added successfully!" + Fore.RESET)
        elif choice == '4':
            add_subcategory()
            print(Fore.GREEN + "Subcategory added successfully!" + Fore.RESET)
        elif choice == '5':
            user_login()
        elif choice == '6':
            add_expenses()
        elif choice == '7':
            stats()
        elif choice == '8':
            print("Exiting the program.")
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again." + Fore.RESET)


if __name__ == "__main__":
    main()

import sqlite3
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

def add_category():
    category_name = input("Enter category: ")
    
    conn = connect_to_database()
    c = conn.cursor()
    c.execute("INSERT INTO category (category_name) VALUES (?)", (category_name,))
    conn.commit()
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
        print(Fore.GREEN + "2. Add new task" + Fore.RESET)
        print(Fore.RED + "3. Login task" + Fore.RESET)
        print(Fore.LIGHTMAGENTA_EX + "4. Login expenses" + Fore.RESET)
        print(Fore.MAGENTA + "5. View stats" + Fore.RESET)
        print(Fore.CYAN + "6. Exit" + Fore.RESET)

        choice = input(
            Fore.BLUE + "Enter your choice (1/2/3/4/5/6): " + Fore.RESET)

        if choice == '1':
            add_user()
            print(Fore.GREEN + "User added successfully!" + Fore.RESET)
        elif choice == '2':
            add_task()
            print(Fore.GREEN + "Task added successfully!" + Fore.RESET)
        elif choice == '3':
            user_login()
        elif choice == '4':
            add_expenses()
        elif choice == '5':
            stats()
        elif choice == '6':
            print("Exiting the program.")
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again." + Fore.RESET)


if __name__ == "__main__":
    main()

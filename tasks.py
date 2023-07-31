import sqlite3
from colorama import init, Fore, Style

init(autoreset=True)

def connect_to_database():
    conn = sqlite3.connect('/Users/alessandrazamora/butler/databases/butler_database.db')
    return conn


def close_connection(conn):
    conn.close()


def add_user():
    username = input("Enter the username: ")

    conn = connect_to_database()
    c = conn.cursor()
    c.execute("INSERT INTO users (name) VALUES (?)", (username,))
    conn.commit()
    close_connection(conn)


def add_task():
    task_name = input("Enter the task name: ")

    conn = connect_to_database()
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task_name) VALUES (?)", (task_name,))
    conn.commit()
    close_connection(conn)


def print_welcome():
    art = '''
    ░█████╗░██╗░░░░░███████╗██████╗░███████╗██████╗░
    ██╔══██╗██║░░░░░██╔════╝██╔══██╗██╔════╝██╔══██╗
    ███████║██║░░░░░█████╗░░██████╔╝█████╗░░██║░░██║
    ██╔══██║██║░░░░░██╔══╝░░██╔══██╗██╔══╝░░██║░░██║
    ██║░░██║███████╗██║░░░░░██║░░██║███████╗██████╔╝
    ╚═╝░░╚═╝╚══════╝╚═╝░░░░░╚═╝░░╚═╝╚══════╝╚═════╝░
    '''
    print(Fore.MAGENTA + art + Fore.RESET)
    print(' ')
    print(Fore.BLUE + "Hello. How can I be of service today?" + Fore.RESET)

def main():
    print_welcome()
    while True:
        print(Fore.YELLOW + "1. Add user" + Fore.RESET)
        print(Fore.GREEN + "2. Add task" + Fore.RESET)
        print(Fore.RED + "3. Exit" + Fore.RESET)

        choice = input(Fore.BLUE + "Enter your choice (1/2/3): " + Fore.RESET)

        if choice == '1':
            add_user()
            print(Fore.GREEN + "User added successfully!" + Fore.RESET)
        elif choice == '2':
            add_task()
            print(Fore.GREEN + "Task added successfully!" + Fore.RESET)
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again." + Fore.RESET)


if __name__ == "__main__":
    main()
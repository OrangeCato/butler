from pickle import NONE
import sqlite3
import time
from datetime import datetime
import threading
from colorama import init, Fore

init(autoreset=True)

def connect_to_database(db_path='/Users/alessandrazamora/butler/databases/butler_database.db'):
    conn = sqlite3.connect(db_path)
    return conn

def close_connection(conn):
    conn.close()
    
def get_user_id(username):
    conn = connect_to_database()
    c = conn.cursor()
    c.execute('SELECT id FROM users WHERE name = ?', (username,))
    user_id = c.fetchone()
    close_connection(conn)
    return user_id[0] if user_id else None

def get_tasks():
    conn = connect_to_database()
    c = conn.cursor()
    c.execute('SELECT * FROM tasks')
    tasks_rows = c.fetchall()
    close_connection(conn)
    return tasks_rows

def get_task_id(task_name):
    conn = connect_to_database()
    c = conn.cursor()
    c.execute('SELECT id FROM tasks WHERE task_name = ?', (task_name,))
    task_id = c.fetchone()
    close_connection(conn)
    return task_id[0] if task_id else None

def log_task_completion(user_id, task_id, date_added, total_length):
    conn = connect_to_database()
    c = conn.cursor()
    current_time = datetime.now().strftime('%H:%M')
    c.execute("INSERT INTO logs (user_id, task_id, date, time, length) VALUES (?, ?, ?, ?, ?)",
              (user_id, task_id, date_added, current_time, total_length))
    conn.commit()
    close_connection(conn)

# Prints running timer
def print_timer(start_time, timer_running_event):
    last_time = ""
    while True:
        if timer_running_event.wait(1):
            current_time = time.time()
            elapsed_time = round(current_time - start_time, 2)
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            new_time = f"Time running: {minutes:02d}:{seconds:02d}"
            if new_time != last_time:
                print("\033[K" + Fore.MAGENTA + new_time, end='\r' + Fore.RESET)
                last_time = new_time

# Start task
def start_task(username, user_id):
    print(Fore.GREEN + f"Hello, {username}! Let's start a task." + Fore.RESET)

    tasks = get_tasks()
    print(Fore.YELLOW + "Choose a task from the list or add a new task:" + Fore.RESET)
    for idx, task in enumerate(tasks, start=1):
        print(Fore.BLUE + f"{idx}. {task[1]}" + Fore.RESET)
    print(Fore.YELLOW + "or..." + Fore.RESET)
    print(Fore.YELLOW + "0. Add new task" + Fore.RESET)

    while True:
        choice = input(Fore.CYAN + "Enter the task number:" + Fore.RESET)
        if choice.isdigit() and 0 <= int(choice) <= len(tasks):
            break
        print(Fore.RED + "Invalid choice. Please try again." + Fore.RESET)

    if choice == '0':
        new_task_name = input(Fore.CYAN + "Enter new task:" + Fore.RESET)
        conn = connect_to_database()
        c = conn.cursor()
        c.execute("INSERT INTO tasks (task_name) VALUES (?)", (new_task_name,))
        conn.commit()
        close_connection(conn)
        task_id = get_task_id(new_task_name)
        print(Fore.MAGENTA + f"New task '{new_task_name}' added with ID {task_id}." + Fore.RESET)
    else:
        task_id = tasks[int(choice) - 1][0]
        task_name = tasks[int(choice) - 1][1]
        print(Fore.CYAN + f"Selected task: {task_name}" + Fore.RESET)
        date_added = datetime.now().strftime('%Y-%m-%d')
        start_time = time.time()
        print(Fore.GREEN + "Time started. Press S to stop or F to finish task." + Fore.RESET)
        # Start the timer display
        timer_running_event = threading.Event()
        timer_running_event.set()
        timer_thread = threading.Thread(target=print_timer, args=(start_time, timer_running_event))
        timer_thread.start()

    while True:
        user_input = input()
        if user_input.upper() == 'S':
            timer_running_event.clear()
            stop_time = time.time()
            time_taken = round(stop_time - start_time, 2)
            print(Fore.YELLOW + f"Task stopped at {time_taken} seconds." + Fore.RESET)
            total_length_minutes = int(time_taken // 60)
            log_choice = input(Fore.YELLOW + "Press L to log recorded task, C to resume timer or T to terminate task:" + Fore.RESET)
            if log_choice.upper() == 'L':
                log_id = int(time.time())
                log_task_completion(user_id, task_id, date_added, total_length_minutes)
                print(Fore.GREEN + "Task logged successfully!" + Fore.RESET)
            elif log_choice.upper() == 'C':
                timer_running_event.set()
                print('')
            elif log_choice.upper() == 'T':
                print(Fore.YELLOW + "Log deleted." + Fore.RESET)
            else:
                print(Fore.RED + 'Invalid input. Please try again' + Fore.RESET)
            break
        elif user_input.upper() == 'F':
            timer_running_event.clear()
            stop_time = time.time()
            time_taken = round(stop_time - start_time, 2)
            print(Fore.MAGENTA + f"Task finished, time taken: {time_taken} seconds." + Fore.RESET)
            total_length_minutes = int(time_taken // 60)
            print(Fore.CYAN + f"Total length of the task: {total_length_minutes} minutes." + Fore.RESET)
            log_choice = input(Fore.YELLOW + "Press L to log recorded task or T to terminate task." + Fore.RESET)
            if log_choice.upper() == 'L':
                log_id = int(time.time())
                log_task_completion(user_id, task_id, date_added, total_length_minutes)
                print(Fore.GREEN + "Task logged successfully!" + Fore.RESET)
            elif log_choice.upper() == 'T':
                print(Fore.YELLOW + "Log deleted." + Fore.RESET)
            else:
                print(Fore.RED + 'Invalid input. Please try again.' + Fore.RESET)
            break
        else:
            timer_running_event.set
            print(Fore.RED + "Invalid input. Press S to stop and F to finish task." + Fore.RESET)

    # Join the timer thread to avoid leaving it running
    timer_thread.join()

def main():
    username = input(Fore.MAGENTA + "Enter your username:" + Fore.RESET)
    user_id = get_user_id(username)
    start_task(username, user_id)

if __name__ == "__main__":
    main()

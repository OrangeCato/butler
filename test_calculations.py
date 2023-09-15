import unittest
import os
import sqlite3
import time
from datetime import datetime
from colorama import init, Fore, Style
from task_calculations import connect_to_database, get_task_id, log_task_completion, get_tasks

# Initialize colorama
init()

# Create temporary db for testing
TEMP_DB_PATH = '/Users/alessandrazamora/butler/databases/test_db.db'


class TestCalculations(unittest.TestCase):
    def setUp(self):
        self.conn = connect_to_database(db_path=TEMP_DB_PATH)
        self.create_tables()
        self.insert_test_data()
        self.insert_test_users()
        
    def tearDowClass(self):
        self.conn.close()
        # Delete temporary db after all test have run
        os.remove(TEMP_DB_PATH)

    def setUp(self):
        # before each test, create fresh db with new necessary tables
        self.create_tables()
        self.insert_test_data()
        self.insert_test_users()

    def tearDown(self):
        # After each test rollback any changes and close connection
        self.conn.rollback()

    def create_tables(self):
        c = self.conn.cursor()
        # create tables if they don't exist
        c.execute(
            '''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, task_name TEXT NOT NULL)''')

        c.execute('''CREATE TABLE IF NOT EXISTS logs (log_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, task_id INTEGER, date TEXT, time REAL, length INTEGER)''')
        self.conn.commit()
        
        c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)''')

    def insert_test_data(self):
        c = self.conn.cursor()
        # Insert test data into the tasks table
        c.execute("INSERT INTO tasks (task_name) VALUES (?)", ('Test task 1',))
        c.execute("INSERT INTO tasks (task_name) VALUES (?)", ('Test task 2',))
        self.conn.commit()
        
    def insert_test_users(self):
        c = self.conn.cursor()
        # Insert test users into the users table
        c.execute("INSERT INTO users (name) VALUES (?)", ('Test User 1',))
        c.execute("INSERT INTO users (name) VALUES (?)", ('Test User 2',))
        self.conn.commit()

    def test_get_task_id_existing(self):
        task_id = get_task_id('Test task 1')
        self.assertEqual(
            task_id, 1, f"{Fore.RED}Failed to get task ID for existing task.{Style.RESET_ALL}")

    def test_log_task(self):
        task_id = get_task_id('Test task 2')
        date_added = datetime.now().strftime('%Y-%m-%d')
        start_time = time.time()
        log_task_completion(1, task_id, date_added, start_time, 300)
        # Check if log entry was added to logs table
        c = self.conn.cursor()
        c.execute('SELECT * FROM logs')
        log_entry = c.fetchone()
        self.assertEqual(
            log_entry[1], 1, f"{Fore.RED}Failed to log task completion for uid 1{Style.RESET_ALL}")

    def test_get_tasks(self):
        tasks = get_tasks()
        self.assertEqual(
            len(tasks), 2, f"{Fore.RED}Incorrect tasks retrieved.{Style.RESET_ALL}")
        self.assertEqual(tasks[0][1], 'Test task 1')
        self.assertEqual(tasks[1][1], 'Test task 2')


if __name__ == '__main__':
    unittest.main()

import sqlite3
from datetime import datetime
from colorama import init, Fore
from task_calculations import get_user_id

init(autoreset=True)

# Constants for table and column names
CATEGORIES_TABLE = "categories"
CATEGORY_ID_COLUMN = "category_id"
CATEGORY_NAME_COLUMN = "category_name"

EXPENSES_TABLE = "expenses"
EXPENSE_ID_COLUMN = "expense_id"
USER_ID_COLUMN = "user_id"
CATEGORY_ID_COLUMN_EXPENSES = "category_id"
SUBCATEGORY_ID_COLUMN = "subcategory_id"
AMOUNT_COLUMN = "amount"
DATE_COLUMN = "date"

LOGS_TABLE = "logs"
USER_ID_LOG_COLUMN = "user_id"
LOG_ID_COLUMN = "log_id"
TASK_ID_COLUMN = "task_id"
TIME_COLUMN = "time"
LENGTH_COLUMN = "length"
CATEGORY_ID_COLUMN_LOGS = "category_id"
SUBCATEGORY_ID_COLUMN_LOGS = "subcategory_id"
AMOUNT_COLUMN_LOGS = "amount"

SUBCATEGORIES_TABLE = "subcategories"
SUBCATEGORY_ID_COLUMN_SUBCATEGORIES = "subcategory_id"
SUBCATEGORY_NAME_COLUMN = "subcategory_name"
CATEGORY_ID_COLUMN_SUBCATEGORIES = "category_id"

USERS_TABLE = "users"
USER_ID_COLUMN_USERS = "id"
USERNAME_COLUMN = "name"


def connect_to_database(db_path='/Users/alessandrazamora/butler/databases/butler_database.db'):
    conn = sqlite3.connect(db_path)
    return conn


def close_connection(conn):
    conn.close()


def get_categories(conn):
    c = conn.cursor()
    c.execute(f'SELECT * FROM {CATEGORIES_TABLE}')
    category_rows = c.fetchall()
    return category_rows


def get_subcategories(conn, category_id):
    c = conn.cursor()
    c.execute(
        f'SELECT * FROM {SUBCATEGORIES_TABLE} WHERE {CATEGORY_ID_COLUMN} = ?', (category_id,))
    subcategories_rows = c.fetchall()
    return subcategories_rows


def get_category_id(conn, category_name):
    c = conn.cursor()
    c.execute(
        f'SELECT {CATEGORY_ID_COLUMN} FROM {CATEGORIES_TABLE} WHERE {CATEGORY_NAME_COLUMN} = ?', (category_name,))
    category_id = c.fetchone()
    return category_id[0] if category_id else None


def get_subcategory_id(conn, subcategory_name):
    c = conn.cursor()
    c.execute(
        f'SELECT {SUBCATEGORY_ID_COLUMN} FROM {SUBCATEGORIES_TABLE} WHERE {SUBCATEGORY_NAME_COLUMN} = ?', (subcategory_name,))
    subcategory_id = c.fetchone()
    return subcategory_id[0] if subcategory_id else None


def add_category(conn, category_name):
    c = conn.cursor()
    c.execute(
        f"INSERT INTO {CATEGORIES_TABLE} ({CATEGORY_NAME_COLUMN}) VALUES (?)", (category_name,))
    conn.commit()


def add_subcategory(conn, subcategory_name, category_id):
    c = conn.cursor()
    c.execute(
        f"INSERT INTO {SUBCATEGORIES_TABLE} ({SUBCATEGORY_NAME_COLUMN}, {CATEGORY_ID_COLUMN}) VALUES (?, ?)", (subcategory_name, category_id))
    conn.commit()


def add_expense(conn, user_id, category_id, subcategory_id, amount, date):
    c = conn.cursor()
    current_time = datetime.now().strftime('%H:%M')
    c.execute(
        f"INSERT INTO {LOGS_TABLE} ({USER_ID_LOG_COLUMN}, {CATEGORY_ID_COLUMN}, {SUBCATEGORY_ID_COLUMN_LOGS}, {DATE_COLUMN}, {TIME_COLUMN}, {AMOUNT_COLUMN_LOGS}) VALUES (?,?,?,?,?,?)",
        (user_id, category_id, subcategory_id, date, current_time, amount))
    conn.commit()


def is_valid_amount(amount_str):
    try:
        amount = float(amount_str)
        return amount >= 0
    except ValueError:
        return False


def start_expense_log(username, user_id):
    print(Fore.GREEN +
          f"Hello, {username}! Let's add an expense. Choose from the following:" + Fore.RESET)

    conn = connect_to_database()
    category_id = None
    subcategory_id = None

    while True:
        categories = get_categories(conn)
        for idx, category in enumerate(categories, start=1):
            print(f"{idx}. {category[1]}")

        print(Fore.YELLOW + "or...")
        print(Fore.YELLOW + "0. Add new category" + Fore.RESET)
        print(Fore.RED + "X. Cancel" + Fore.RESET)

        choice = input(
            Fore.CYAN + "Enter number(or X to cancel): " + Fore.RESET)

        if choice == '0':
            new_category_name = input(
                Fore.CYAN + "Enter the new category name: " + Fore.RESET)
            add_category(conn, new_category_name)
            category_id = get_category_id(conn, new_category_name)
            print(
                Fore.MAGENTA + f"New category '{new_category_name}' added with ID {category_id}." + Fore.RESET)
        elif choice == 'X':
            print(Fore.RED + "Expense log canceled." + Fore.RESET)
            break  # Exit the loop when canceled
        elif choice.isdigit() and 1 <= int(choice) <= len(categories):
            category_id = categories[int(choice) - 1][0]
            category_name = categories[int(choice) - 1][1]
            print(Fore.CYAN +
                  f"Selected category: {category_name}" + Fore.RESET)

            subcategories = get_subcategories(conn, category_id)
            print(Fore.LIGHTMAGENTA_EX +
                  "Choose from the list of the selected category:" + Fore.RESET)
            for idx, subcategory in enumerate(subcategories, start=1):
                print(f"{idx}. {subcategory[1]}")

            print(Fore.YELLOW + "or...")
            print(Fore.YELLOW + "0. Add new subcategory" + Fore.RESET)
            print(Fore.RED + "X. Cancel" + Fore.RESET)

            subcategory_choice = input(
                Fore.CYAN + "Enter number (or X to cancel): " + Fore.RESET)

            if subcategory_choice == '0':
                new_subcategory_name = input(
                    Fore.CYAN + "Enter the new subcategory name: " + Fore.RESET)
                add_subcategory(conn, new_subcategory_name, category_id)
                subcategory_id = get_subcategory_id(conn, new_subcategory_name)
                print(
                    Fore.MAGENTA + f"New subcategory '{new_subcategory_name}' added with ID {subcategory_id}." + Fore.RESET)
            elif subcategory_choice == 'X':
                print(Fore.RED + "Expense log canceled." + Fore.RESET)
                break  # Exit the loop when canceled
            elif subcategory_choice.isdigit() and 1 <= int(subcategory_choice) <= len(subcategories):
                subcategory_id = subcategories[int(subcategory_choice) - 1][0]
                subcategory_name = subcategories[int(
                    subcategory_choice) - 1][1]
                print(Fore.CYAN +
                      f"Selected subcategory: {subcategory_name}" + Fore.RESET)
            else:
                print(Fore.RED + "Invalid choice. Please try again." + Fore.RESET)

        # Ask for the amount spent and log the expense
        while True:
            amount_str = input(
                Fore.CYAN + "Enter the amount spent (e.g., 25.50): " + Fore.RESET)

            if is_valid_amount(amount_str):
                amount = float(amount_str)
                break
            else:
                print(
                    Fore.RED + "Invalid amount format. Please enter a valid amount." + Fore.RESET)

        date = datetime.now().strftime('%Y-%m-%d')
        add_expense(conn, user_id, category_id, subcategory_id, amount, date)
        print(Fore.MAGENTA +
              f"Expense of ${amount:.2f} logged for category '{category_name}', subcategory '{subcategory_name}' on {date}." + Fore.RESET)

    close_connection(conn)  # Close the connection when done


def main():
    username = input(Fore.MAGENTA + "Enter your username:" + Fore.RESET)
    user_id = get_user_id(username)
    start_expense_log(username, user_id)


if __name__ == '__main__':
    main()

    '''
    expense_categories = {
    'Housing': ['Rent/Mortgage', 'Utilities', 'Property Taxes', 'Home Repairs and Maintenance', 'Home Insurance'],
    'Transportation': ['Car Payments', 'Gasoline/Fuel', 'Public Transportation', 'Car Insurance', 'Maintenance and Repairs'],
    'Food': ['Groceries', 'Dining Out', 'Takeout and Delivery'],
    'Utilities': ['Internet', 'Cable or Satellite TV', 'Mobile Phone Plans', 'Landline Phone'],
    'Insurance': ['Health Insurance', 'Life Insurance', 'Disability Insurance', 'Other Insurance'],
    'Debt Payments': ['Credit Card Payments', 'Personal Loans', 'Student Loans', 'Other Loan Payments'],
    'Entertainment': ['Movies', 'Concerts and Events', 'Hobbies and Recreation', 'Subscriptions', 'Books and Magazines'],
    'Personal Care': ['Haircuts and Grooming', 'Toiletries and Cosmetics', 'Gym Memberships', 'Spa and Wellness'],
    'Healthcare': ['Doctor\'s Visits', 'Prescriptions and Medications', 'Dental and Vision Care', 'Health Supplements'],
    'Education': ['Tuition and School Fees', 'Books and Supplies', 'Educational Courses'],
    'Savings and Investments': ['Retirement Savings', 'Emergency Fund Contributions', 'Investments', 'Other Savings Goals'],
    'Charity and Donations': ['Donations to Nonprofits', 'Charitable Contributions'],
    'Taxes': ['Income Taxes', 'Property Taxes', 'Other Taxes'],
    'Travel': ['Flights', 'Accommodation', 'Transportation at the Destination', 'Activities and Excursions'],
    'Gifts and Special Occasions': ['Birthdays', 'Anniversaries', 'Holidays', 'Wedding Gifts'],
    'Miscellaneous': ['Any other expenses not covered by the above categories']
}
'''

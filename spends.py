import sqlite3
from datetime import datetime
from colorama import init, Fore
from Calculations import get_user_id

init(autoreset=True)

# Constants for table and column names
EXPENSES_TABLE = "expenses"
CATEGORIES_COLUMN = "categories"
CATEGORY_ID_COLUMN = "category_id"
AMOUNT_COLUMN = "amount"
DATE_COLUMN = "date"

USERS_TABLE = "users"
USER_ID_COLUMN = "id"
USERNAME_COLUMN = "name"

LOGS_TABLE = "logs"
LOG_ID_COLUMN = "log_id"
USER_ID_LOG_COLUMN = "user_id"
TIME_COLUMN = "time"


def connect_to_database(db_path='/Users/alessandrazamora/butler/databases/butler_database.db'):
    conn = sqlite3.connect(db_path)
    return conn


def close_connection(conn):
    conn.close()


def get_categories(conn):
    c = conn.cursor()
    c.execute(f'SELECT * FROM {EXPENSES_TABLE}')
    category_rows = c.fetchall()
    return category_rows


def get_category_id(conn, category_name):
    c = conn.cursor()
    c.execute(
        f'SELECT {CATEGORY_ID_COLUMN} FROM {EXPENSES_TABLE} WHERE {CATEGORIES_COLUMN} = ?', (category_name,))
    category_id = c.fetchone()
    return category_id[0] if category_id else None


def add_category(conn, category_name):
    c = conn.cursor()
    c.execute(
        f"INSERT INTO {EXPENSES_TABLE} ({CATEGORIES_COLUMN}) VALUES (?)", (category_name,))
    conn.commit()


def add_expense(conn, user_id, category_id, amount, date_added):
    c = conn.cursor()
    current_time = datetime.now().strftime('%H:%M')
    c.execute(f"INSERT INTO {LOGS_TABLE} ({USER_ID_LOG_COLUMN}, {CATEGORY_ID_COLUMN}, {DATE_COLUMN}, {TIME_COLUMN}, {AMOUNT_COLUMN}) VALUES (?,?,?,?,?)",
              (user_id, category_id, date_added, current_time, amount))
    conn.commit()


def is_valid_amount(amount_str):
    try:
        amount = float(amount_str)
        return amount >= 0
    except ValueError:
        return False


def start_expense_log(username, user_id):
    print(Fore.GREEN +
          f"Hello, {username}! Let's add an expense." + Fore.RESET)

    # Display existing categories and allow adding a new one
    conn = connect_to_database()
    categories = get_categories(conn)  # Retrieve categories initially

    category_name = None  # Initialize category_name outside the loop

    while True:
        for idx, category in enumerate(categories, start=1):
            print(Fore.LIGHTMAGENTA_EX + f"{idx}. {category[1]}" + Fore.RESET)

        print(Fore.YELLOW + "0. Add new category" + Fore.RESET)
        print(Fore.YELLOW + "or..." + Fore.RESET)
        print(Fore.RED + "X. Cancel" + Fore.RESET)

        choice = input(
            Fore.CYAN + "Enter category number (0 to add new, X to cancel): " + Fore.RESET)

        if choice == '0':
            new_category_name = input(
                Fore.CYAN + "Enter the new category name: " + Fore.RESET)
            add_category(conn, new_category_name)
            category_id = get_category_id(conn, new_category_name)
            category_name = new_category_name  # Set the category_name to the new category
            print(
                Fore.MAGENTA + f"New category '{new_category_name}' added with ID {category_id}." + Fore.RESET)
            # Update categories after adding a new one
            categories = get_categories(conn)
            break
        elif choice == 'X':
            print(Fore.RED + "Expense log canceled." + Fore.RESET)
            close_connection(conn)
            return
        elif choice.isdigit() and 1 <= int(choice) <= len(categories):
            category_id = categories[int(choice) - 1][0]
            category_name = categories[int(choice) - 1][1]
            print(Fore.CYAN +
                  f"Selected category: {category_name}" + Fore.RESET)
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again." + Fore.RESET)

    # Ask for the amount spent
    while True:
        amount_str = input(
            Fore.CYAN + "Enter the amount spent (e.g., 25.50): " + Fore.RESET)

        if is_valid_amount(amount_str):
            amount = float(amount_str)
            break
        else:
            print(
                Fore.RED + "Invalid amount format. Please enter a valid amount." + Fore.RESET)

    # Log the expense
    date = datetime.now().strftime('%Y-%m-%d')
    add_expense(conn, user_id, category_id, amount, date)
    print(Fore.MAGENTA +
          f"Expense of ${amount:.2f} logged for category '{category_name}' on {date}." + Fore.RESET)
    close_connection(conn)


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

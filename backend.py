# backend.py
import sqlite3

# Function to create a connection to the SQLite database
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to SQLite database version: {sqlite3.version}")
    except sqlite3.Error as e:
        print(e)
    return conn

# Function to create the user table
def create_user_table(conn):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        age INTEGER NOT NULL,
        income REAL NOT NULL,
        expenses REAL NOT NULL,
        retirement_age INTEGER NOT NULL,
        desired_income REAL NOT NULL,
        rrsp_amount REAL NOT NULL,
        tfsa_amount REAL NOT NULL,
        non_registered_amount REAL NOT NULL,
        credit_card_debt REAL NOT NULL,
        student_loan_debt REAL NOT NULL,
        personal_loan_debt REAL NOT NULL,
        risk_tolerance TEXT NOT NULL,
        repayment_strategy TEXT NOT NULL
    );
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

# Function to insert user data into the database
def insert_user_data(conn, user_data):
    sql = """
    INSERT INTO users(age, income, expenses, retirement_age, desired_income, rrsp_amount, tfsa_amount, non_registered_amount,
                      credit_card_debt, student_loan_debt, personal_loan_debt, risk_tolerance, repayment_strategy)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    try:
        cur = conn.cursor()
        cur.execute(sql, user_data)
        conn.commit()
        return cur.lastrowid
    except sqlite3.Error as e:
        print(e)

# Function to retrieve user data from the database
def get_user_data(conn, user_id):
    sql = "SELECT * FROM users WHERE id = ?"
    cur = conn.cursor()
    cur.execute(sql, (user_id,))
    return cur.fetchone()

# Example usage
if __name__ == "__main__":
    database = "financial_planning.db"
    conn = create_connection(database)
    create_user_table(conn)

    # Example of inserting user data
    user_data = (30, 5000, 3000, 65, 10000, 20000, 15000, 10000, 5000, 10000, 5000, "medium", "debt snowball")
    user_id = insert_user_data(conn, user_data)
    print(f"User ID: {user_id}")

    # Example of retrieving user data
    user = get_user_data(conn, user_id)
    print("User Data:", user)

    conn.close()

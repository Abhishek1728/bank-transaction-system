from datetime import datetime
import os
import re
import sys
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

print("***** BANK TRANSACTION SYSTEM *****")

# ---------- LIMITS (change these numbers if you want different rules) ----------
ACC_MIN_DIGITS = 6          # account number: minimum digits
ACC_MAX_DIGITS = 12         # account number: maximum digits
NAME_MAX_LEN = 50           # name: maximum characters (database allows 100)
CITY_MAX_LEN = 30           # city: maximum characters (database allows 50)
MOBILE_DIGITS = 10          # mobile number: exact digits
MAX_TRANSACTION = 1000000   # maximum amount in one deposit / withdrawal
MAX_LOAN = 1000000          # maximum loan amount
MAX_BALANCE = 2000000000    # balance can never go above this (database INT limit)

# Reads DB_HOST, DB_USER, DB_PASSWORD, DB_NAME from the .env file
load_dotenv()

# ---------- MYSQL CONNECTION ----------
try:
    mydb = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "bank")
    )
except Error as e:
    print("Could not connect to MySQL:", e)
    print("Check that MySQL is running, your .env file is in the same folder,")
    print("and the password in .env is correct.")
    sys.exit(1)

mycursor = mydb.cursor()


# ---------- INPUT HELPER FUNCTIONS ----------
def get_account(prompt="Enter account number: "):
    """Account number: digits only, ACC_MIN_DIGITS to ACC_MAX_DIGITS long."""
    while True:
        value = input("{}({}-{} digits): ".format(
            prompt.rstrip(": "), ACC_MIN_DIGITS, ACC_MAX_DIGITS)).strip()
        if value.isdigit() and ACC_MIN_DIGITS <= len(value) <= ACC_MAX_DIGITS:
            return value
        print("Invalid account number. Use digits only, {} to {} digits long."
              .format(ACC_MIN_DIGITS, ACC_MAX_DIGITS))


def get_name(prompt, max_len):
    """Letters and spaces only (also . ' -), cannot be empty, limited length."""
    while True:
        value = input("{}(max {} letters): ".format(prompt.rstrip(": "), max_len)).strip()
        if not value:
            print("This field cannot be empty.")
        elif len(value) > max_len:
            print("Too long. Maximum {} characters.".format(max_len))
        elif not re.fullmatch(r"[A-Za-z][A-Za-z .'\-]*", value):
            print("Use letters and spaces only (no numbers or symbols).")
        else:
            return value


def get_mobile(prompt="Enter mobile number: "):
    """Exactly MOBILE_DIGITS digits, starting with 6, 7, 8 or 9."""
    while True:
        value = input("{}({} digits): ".format(prompt.rstrip(": "), MOBILE_DIGITS)).strip()
        if value.isdigit() and len(value) == MOBILE_DIGITS and value[0] in "6789":
            return value
        print("Invalid mobile number. Enter exactly {} digits, starting with 6, 7, 8 or 9."
              .format(MOBILE_DIGITS))


def get_amount(prompt, max_amount):
    """Whole number from 1 up to max_amount."""
    while True:
        value = input("{}(1-{}): ".format(prompt.rstrip(": "), max_amount)).strip()
        if not value.isdigit():
            print("Please enter a whole number (digits only, no minus sign or decimals).")
            continue
        number = int(value)
        if number < 1:
            print("Amount must be greater than 0.")
        elif number > max_amount:
            print("Amount too large. Maximum allowed is {}.".format(max_amount))
        else:
            return number


def get_date(prompt):
    """Ask for a date in YYYY-MM-DD format. Press Enter to use today's date."""
    while True:
        value = input(prompt + " (YYYY-MM-DD, press Enter for today): ").strip()
        if value == "":
            return datetime.now().strftime("%Y-%m-%d")
        try:
            entered = datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            print("Invalid date. Use the format YYYY-MM-DD, e.g. 2026-09-30.")
            continue
        if entered.date() > datetime.now().date():
            print("Date cannot be in the future.")
            continue
        return value


def account_exists(acno):
    mycursor.execute("SELECT * FROM bank_master WHERE acno = %s", (acno,))
    return mycursor.fetchone()


# ---------- MAIN MENU ----------
try:
    while True:

        print("\n1 = Create Account")
        print("2 = Deposit Money")
        print("3 = Withdraw Money")
        print("4 = Display Account Details")
        print("5 = Take Loan")
        print("6 = Exit")

        choice = input("Enter your choice (1-6): ").strip()

        if not choice.isdigit():
            print("Please enter a number from 1 to 6.")
            continue

        ch = int(choice)

        try:
            # ---------- CREATE ACCOUNT ----------
            if ch == 1:
                print("\n-------- CREATE ACCOUNT --------")

                acno = get_account()

                if account_exists(acno) is not None:
                    print("Account number already exists")
                else:
                    name = get_name("Enter name: ", NAME_MAX_LEN)
                    city = get_name("Enter city: ", CITY_MAX_LEN)
                    mn = get_mobile()

                    try:
                        mycursor.execute(
                            "INSERT INTO bank_master VALUES (%s, %s, %s, %s, 0, 0, '0')",
                            (acno, name, city, mn)
                        )
                        mydb.commit()
                        print("Account created successfully")
                    except mysql.connector.errors.IntegrityError:
                        mydb.rollback()
                        print("Account number already exists")

            # ---------- DEPOSIT ----------
            elif ch == 2:
                print("\n-------- DEPOSIT --------")

                acno = get_account()
                data = account_exists(acno)

                if data is None:
                    print("Account does not exist")
                else:
                    amt = get_amount("Enter deposit amount: ", MAX_TRANSACTION)

                    if data[4] + amt > MAX_BALANCE:
                        print("Deposit not allowed: balance would exceed the maximum limit.")
                    else:
                        dot = get_date("Enter date")

                        try:
                            mycursor.execute(
                                "INSERT INTO banktransaction VALUES (%s, %s, %s, 'D')",
                                (acno, amt, dot)
                            )
                            mycursor.execute(
                                "UPDATE bank_master SET balance = balance + %s WHERE acno = %s",
                                (amt, acno)
                            )
                            mydb.commit()
                            print("Amount deposited successfully")
                        except Error as e:
                            mydb.rollback()
                            print("Deposit failed:", e)

            # ---------- WITHDRAW ----------
            elif ch == 3:
                print("\n-------- WITHDRAW MONEY --------")

                acno = get_account()
                data = account_exists(acno)

                if data is None:
                    print("Account does not exist")
                else:
                    balance = data[4]
                    print("Current balance:", balance)

                    if balance == 0:
                        print("Insufficient balance")
                    else:
                        amt = get_amount("Enter withdrawal amount: ", MAX_TRANSACTION)

                        if amt > balance:
                            print("Insufficient balance")
                        else:
                            dot = get_date("Enter date")

                            try:
                                mycursor.execute(
                                    "INSERT INTO banktransaction VALUES (%s, %s, %s, 'W')",
                                    (acno, amt, dot)
                                )
                                mycursor.execute(
                                    "UPDATE bank_master SET balance = balance - %s WHERE acno = %s",
                                    (amt, acno)
                                )
                                mydb.commit()
                                print("Amount withdrawn successfully")
                            except Error as e:
                                mydb.rollback()
                                print("Withdrawal failed:", e)

            # ---------- DISPLAY ACCOUNT DETAILS ----------
            elif ch == 4:
                print("\n-------- ACCOUNT DETAILS --------")

                acno = get_account()
                data = account_exists(acno)

                if data is None:
                    print("Account does not exist")
                else:
                    print("\nAccount Number :", data[0])
                    print("Name           :", data[1])
                    print("City           :", data[2])
                    print("Mobile Number  :", data[3])
                    print("Balance        :", data[4])
                    print("Loan Amount    :", data[5])
                    print("Loan Status    :", data[6])

                    print("\n-------- TRANSACTIONS --------")

                    mycursor.execute(
                        "SELECT * FROM banktransaction WHERE acno = %s ORDER BY dot",
                        (acno,)
                    )
                    transactions = mycursor.fetchall()

                    if len(transactions) == 0:
                        print("No transactions found")
                    else:
                        for row in transactions:
                            kind = "Deposit" if row[3] == "D" else "Withdrawal"
                            print("Account:", row[0],
                                  "| Amount:", row[1],
                                  "| Date:", row[2],
                                  "| Type:", kind)

            # ---------- TAKE LOAN ----------
            elif ch == 5:
                print("\n-------- TAKE LOAN --------")

                acno = get_account()
                data = account_exists(acno)

                if data is None:
                    print("Account does not exist")
                elif data[5] != 0:
                    print("Loan already taken")
                else:
                    loan = get_amount("Enter loan amount: ", MAX_LOAN)

                    if data[4] + loan > MAX_BALANCE:
                        print("Loan not allowed: balance would exceed the maximum limit.")
                    else:
                        try:
                            # Record the loan AND credit the amount to the balance
                            mycursor.execute(
                                "UPDATE bank_master "
                                "SET loan = %s, loan_status = '1', balance = balance + %s "
                                "WHERE acno = %s",
                                (loan, loan, acno)
                            )
                            mydb.commit()
                            print("Loan taken successfully")
                            print("Loan Amount :", loan)
                        except Error as e:
                            mydb.rollback()
                            print("Loan failed:", e)

            # ---------- EXIT ----------
            elif ch == 6:
                print("\nThank you for using Bank Transaction System")
                break

            else:
                print("Invalid choice. Enter a number from 1 to 6.")

        except Error as e:
            # Any other database problem: undo partial changes and keep running
            mydb.rollback()
            print("Database error:", e)

except KeyboardInterrupt:
    print("\n\nProgram interrupted. Goodbye!")

finally:
    # Always close the connection, whichever way the program ends
    mycursor.close()
    mydb.close()

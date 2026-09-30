# Bank Transaction System

A command-line banking application written in **Python** that stores its data in a **MySQL** database. From a terminal menu you can create accounts, deposit and withdraw money, view account details with transaction history, and take a loan. No graphical interface is needed.

## Features

| Menu option | What it does |
|---|---|
| 1. Create Account | Registers an account (number, name, city, mobile). Starts with balance 0. Duplicate account numbers are rejected. |
| 2. Deposit Money | Adds money to an account and records the transaction with a date. |
| 3. Withdraw Money | Removes money if the balance is enough and records the transaction. |
| 4. Display Account Details | Shows holder details, balance, loan info and all transactions. |
| 5. Take Loan | One loan per account; the amount is credited to the balance. |
| 6. Exit | Closes the program and the database connection safely. |

Every input is validated (account number, name, city, mobile number, amounts, dates), and deposits/withdrawals are saved atomically (transaction row and balance update together, or not at all).

## Project Structure

```
.
├── bank.py            # the application
├── schema.sql         # creates the database and tables
├── requirements.txt   # Python dependencies
├── .env.example       # template for database credentials
├── .gitignore         # keeps your real .env out of Git
└── README.md
```

> If your main file has a different name, replace `bank.py` with that name in the commands below.

## Prerequisites

You need these installed before starting:

1. **Python 3.8 or newer** (check with `python --version`, or `python3 --version` on macOS/Linux).
2. **MySQL Server 8.x** (or 5.7+) that is **running**, and the `mysql` command-line client that comes with it.
3. **Git**, to clone the repository.

You also need a MySQL user and password that can create databases (the default `root` user works).

## Setup and Run (step by step)

All commands are typed in a terminal (Command Prompt or PowerShell on Windows, Terminal on macOS/Linux).

### Step 1: Get the code

```bash
git clone <repository-url>
cd <repository-folder>
```

### Step 2: Create and activate a virtual environment (recommended)

Windows (Command Prompt / PowerShell):

```bash
python -m venv venv
venv\Scripts\activate
```

macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

You should now see `(venv)` at the start of your terminal line.

### Step 3: Install the dependencies

```bash
pip install -r requirements.txt
```

This installs `mysql-connector-python` (talks to MySQL) and `python-dotenv` (reads the `.env` file).

### Step 4: Create the database and tables

Make sure MySQL Server is running, then run:

```bash
mysql -u root -p < schema.sql
```

Enter your MySQL password when asked. This creates a database named `bank` with two tables, `bank_master` and `banktransaction`. It is safe to run more than once.

**If you get `'mysql' is not recognized` (Windows):** the MySQL `bin` folder is not on your PATH. Either run it with the full path, for example:

```bash
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p < schema.sql
```

or open the client with `mysql -u root -p` (using the full path) and then type `SOURCE schema.sql;`.

### Step 5: Configure your database credentials

Copy the template to a real `.env` file.

Windows:

```bash
copy .env.example .env
```

macOS / Linux:

```bash
cp .env.example .env
```

Open `.env` in any text editor and fill in your values:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=bank
```

The `.env` file must be in the **same folder as `bank.py`**. It is listed in `.gitignore`, so your password is never uploaded to GitHub.

### Step 6: Run the program

```bash
python bank.py
```

(On macOS/Linux use `python3 bank.py` if `python` is not found.)

You should see the menu:

```
***** BANK TRANSACTION SYSTEM *****

1 = Create Account
2 = Deposit Money
3 = Withdraw Money
4 = Display Account Details
5 = Take Loan
6 = Exit
Enter your choice (1-6):
```

Type a number and press Enter. Choose `6` to exit (or press `Ctrl+C`).

## Quick Test Walkthrough

Follow this to confirm everything works:

1. Choose **1**, then enter account number `100200`, name `Asha Verma`, city `Pune`, mobile `9876543210`. You should see *Account created successfully*.
2. Choose **2**, account `100200`, amount `5000`, press Enter for today's date. You should see *Amount deposited successfully*.
3. Choose **3**, account `100200`, amount `1500`, press Enter for the date. You should see *Amount withdrawn successfully*.
4. Choose **4**, account `100200`. You should see balance `3500` and two transactions.
5. Choose **5**, account `100200`, loan `10000`. The balance becomes `13500`.
6. Choose **6** to exit.

## Input Rules

| Field | Rule |
|---|---|
| Account number | Digits only, 6 to 12 digits |
| Name | Letters, spaces and `. ' -` only, up to 50 characters |
| City | Same as name, up to 30 characters |
| Mobile number | Exactly 10 digits, starting with 6, 7, 8 or 9 |
| Deposit / Withdrawal | Whole number, 1 to 1,000,000 |
| Loan | Whole number, 1 to 1,000,000; one loan per account |
| Date | `YYYY-MM-DD`, not in the future; press Enter for today |
| Balance | Cannot exceed 2,000,000,000 |

These limits are constants at the top of `bank.py` and can be changed there.

## Troubleshooting

| Problem | Likely cause and fix |
|---|---|
| `Could not connect to MySQL: ... Access denied` | Wrong `DB_USER` or `DB_PASSWORD` in `.env`. |
| `Could not connect to MySQL: ... Can't connect to MySQL server` | MySQL Server is not running. Start it (Windows: Services app, or `net start MySQL80`; macOS/Linux: start the `mysql` service). |
| `Unknown database 'bank'` | Step 4 was skipped. Run `mysql -u root -p < schema.sql`. |
| `ModuleNotFoundError: No module named 'mysql'` or `'dotenv'` | Dependencies not installed in the active environment. Activate the virtual environment and rerun `pip install -r requirements.txt`. |
| `Table 'bank.bank_master' doesn't exist` | Step 4 did not complete. Rerun it and check for errors. |
| `.env` values seem ignored | `.env` must be in the folder you run the command from, and named exactly `.env` (not `.env.txt`). |

## Tech Stack

- Python 3
- MySQL
- `mysql-connector-python`, `python-dotenv`

## Limitations

- No login or PIN; anyone can operate any account.
- Loans cannot be repaid and carry no interest.
- Amounts are whole numbers only.

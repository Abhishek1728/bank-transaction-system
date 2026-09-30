# Bank Transaction System

A command-line bank management application built with **Python** and **MySQL**. It lets you create accounts, deposit and withdraw money, view account details with transaction history, and take a loan. All data is stored in a MySQL database.

## Features

- Create a new bank account
- Deposit money
- Withdraw money (with insufficient-balance check)
- Display account details and full transaction history
- Take a loan (one loan per account, amount is credited to the balance)
- Input validation on every field, with clear error messages
- Database credentials kept in a `.env` file, not in the source code

## Tech Stack

| Component | Version |
|---|---|
| Python | 3.8 or newer |
| MySQL Server | 8.0.16 or newer |
| mysql-connector-python | latest |
| python-dotenv | latest |

## Project Structure

```
bank-transaction-system/
├── Bank_System.py                       # Main application
├── Creation_and_ExectuionSQL_Code.txt   # SQL script (creates database and tables)
├── requirements.txt                     # Python dependencies
├── .env.example                         # Template for database credentials
├── .gitignore                           # Keeps real .env out of Git
└── README.md
```

## Setup and Run (Step by Step)

### Step 1: Install the prerequisites

1. **Python 3.8+**: download from https://www.python.org/downloads/. During installation, tick **"Add Python to PATH"**.
2. **MySQL Server** and **MySQL Workbench**: download from https://dev.mysql.com/downloads/installer/. During installation, set a password for the `root` user and remember it.
3. **Git** (only if you want to clone the repository): https://git-scm.com/downloads

Check that Python is installed by opening a terminal (Command Prompt on Windows) and running:

```
python --version
```

(On Windows you can also use `py --version`.)

### Step 2: Get the project

Clone the repository (or download it as a ZIP from GitHub using **Code → Download ZIP** and extract it):

```
git clone https://github.com/Abhishek1728/bank-transaction-system.git
cd bank-transaction-system
```

### Step 3: (Optional) Create a virtual environment

This keeps the project's libraries separate from the rest of your system.

```
python -m venv venv
```

Activate it:

- Windows: `venv\Scripts\activate`
- macOS / Linux: `source venv/bin/activate`

### Step 4: Install the dependencies

```
python -m pip install -r requirements.txt
```

On Windows you can use `py -m pip install -r requirements.txt` if `python` is not recognized.

This installs `mysql-connector-python` and `python-dotenv`.

### Step 5: Create the database and tables

1. Make sure the **MySQL server is running**.
2. Open **MySQL Workbench** and connect to your local instance (for example, "Local instance MySQL").
3. Open a new query tab (**File → New Query Tab**).
4. Open `Creation_and_ExectuionSQL_Code.txt` in any text editor, copy **all** of its contents, and paste them into the query tab.
5. Click the **lightning bolt** icon (or press `Ctrl + Shift + Enter`) to run the script.
6. Verify the setup by running:

```sql
USE bank;
SHOW TABLES;
```

You should see two tables: `bank_master` and `banktransaction`.

The script creates:

| Table | Purpose | Columns |
|---|---|---|
| `bank_master` | Account details | `acno`, `name`, `city`, `mn`, `balance`, `loan`, `loan_status` |
| `banktransaction` | Deposit / withdrawal history | `acno`, `amt`, `dot`, `type` (`D` or `W`) |

### Step 6: Configure your database credentials

The program reads its connection details from a file named `.env` in the project folder. This file is **not** included in the repository, so you must create it.

1. Copy the template:
   - Windows (Command Prompt): `copy .env.example .env`
   - macOS / Linux: `cp .env.example .env`
2. Open `.env` in a text editor and fill in your real values:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=bank
```

- `DB_HOST`: usually `localhost`
- `DB_USER`: your MySQL username, usually `root`
- `DB_PASSWORD`: the password you set when installing MySQL
- `DB_NAME`: keep it as `bank`

Rules for the file: no quotes, no spaces around `=`, and the file must be named exactly `.env` (not `.env.txt`).

### Step 7: Run the application

```
python Bank_System.py
```

(On Windows: `py Bank_System.py`. You can also open the file in IDLE and press `F5`.)

If everything is set up correctly, you will see:

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

## How to Use

Type the number of the option you want and press Enter. A suggested first run:

1. Choose **1** to create an account (for example, account number `100001`).
2. Choose **2** to deposit money (for example, `5000`).
3. Choose **3** to withdraw money (for example, `1000`).
4. Choose **4** to view the account details. The balance should be `4000` with two transactions listed.
5. Choose **5** to take a loan. The amount is added to the balance.
6. Choose **6** to exit.

### Input rules

| Input | Rule |
|---|---|
| Account number | Digits only, 6 to 12 digits |
| Name | Letters and spaces only, up to 50 characters |
| City | Letters and spaces only, up to 30 characters |
| Mobile number | Exactly 10 digits, starting with 6, 7, 8 or 9 |
| Deposit / withdrawal | Whole number from 1 to 1,000,000 |
| Loan | Whole number from 1 to 1,000,000, one loan per account |
| Date | `YYYY-MM-DD`, not in the future. Press Enter to use today's date |

These limits are defined in one block at the top of `Bank_System.py` and can be changed there.

## Troubleshooting

| Problem | Solution |
|---|---|
| `Could not connect to MySQL: Access denied for user` | The password in `.env` is wrong. Use the password you set during MySQL installation. |
| `Could not connect to MySQL: Unknown database 'bank'` | The SQL script has not been run yet. Complete Step 5. |
| `Could not connect to MySQL: Can't connect to MySQL server` | The MySQL server is not running. Start it (Windows: open Services and start MySQL, or use MySQL Workbench). |
| `ModuleNotFoundError: No module named 'dotenv'` or `'mysql'` | Dependencies are not installed. Run Step 4 using the same Python you use to run the program. |
| `pip is not recognized` | Use `python -m pip ...` or `py -m pip ...` instead of `pip ...`. |
| Password is empty or not picked up | The `.env` file is missing, misnamed (for example `.env.txt`), or saved in a different folder than `Bank_System.py`. |

## Security Notes

- The real `.env` file contains your password and is listed in `.gitignore`, so it is never uploaded to GitHub. Never commit it.
- All SQL queries use parameterized statements (`%s` placeholders), which protects against SQL injection.

## Author

Abhishek Jha

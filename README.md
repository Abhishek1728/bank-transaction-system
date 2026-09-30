🏦 Bank Transaction System
A Python + MySQL console app for basic banking — account creation, deposits, withdrawals, balance check, and loans — with input validation and safe SQL.

https://img.shields.io/badge/Python-3.8+-blue https://img.shields.io/badge/MySQL-8.0+-orange https://img.shields.io/badge/License-MIT-green

📌 Overview
CLI banking simulator built with Python + MySQL. Demonstrates CRUD, validation, and transactional integrity. Great for DBMS mini-projects.

✨ Features
#	Feature	Description
1	Create Account	Register customer with validation
2	Deposit	Add funds with caps
3	Withdraw	Balance check + limits
4	Check Balance	Show holder + balance
5	Apply Loan	Credit loan to account
6	Validation	Regex + length checks
7	Safe SQL	Parameterized queries
🧠 Theory & Principles
ACID — Deposits/withdrawals update balance + log transaction atomically.

Layered Design — CLI → Logic → Validation → DB.

Validation — Regex, digit checks, range limits before DB access.

Defensive Programming — try/except + finally for safe cleanup.

SQL Injection Safe — %s placeholders, never string concat.

🛠 Tech Stack
Layer	Tech
Language	Python 3.8+
Database	MySQL 8.0+
Connector	mysql-connector-python
Config	python-dotenv
📁 Structure
text
bank-transaction-system/
├── main.py
├── .env
├── requirements.txt
├── schema.sql
└── README.md
⚙️ Setup
bash
git clone https://github.com/your-username/bank-transaction-system.git
cd bank-transaction-system
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
mysql -u root -p < schema.sql
python main.py
.env

env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=bank_db
🗄 Schema
sql
CREATE TABLE accounts (
    account_number VARCHAR(12) PRIMARY KEY,
    name VARCHAR(100), city VARCHAR(50),
    mobile VARCHAR(10), balance DECIMAL(15,2) DEFAULT 0,
    created_at DATETIME
);
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_number VARCHAR(12), type ENUM('DEPOSIT','WITHDRAW'),
    amount DECIMAL(15,2), timestamp DATETIME,
    FOREIGN KEY (account_number) REFERENCES accounts(account_number)
);
CREATE TABLE loans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_number VARCHAR(12), amount DECIMAL(15,2),
    timestamp DATETIME,
    FOREIGN KEY (account_number) REFERENCES accounts(account_number)
);
🧾 Execution Table
Opt	Function	Input	Validation	DB Action	Output
1	create_account	Acc, Name, City, Mobile	validate_*	INSERT accounts	"Account created"
2	deposit	Acc, Amount	validate_amount	UPDATE + INSERT txn	"New balance: X"
3	withdraw	Acc, Amount	validate_amount + balance	UPDATE + INSERT txn	"New balance: X"
4	check_balance	Acc	validate_account	SELECT	Name + Balance
5	apply_loan	Acc, Amount	validate_amount	UPDATE + INSERT loan	"Loan approved"
6	exit	—	—	—	Exit
Failure Paths

Case	Result
Bad acc/name/mobile	Error, abort
Amount > limit	Error, abort
Insufficient balance	"Insufficient balance"
Account missing	"Account not found"
Balance overflow	Reject txn
📏 Validation Rules
Field	Rule
Account No	6–12 digits
Name	≤ 50 chars, letters + . ' -
City	≤ 30 chars
Mobile	Exactly 10 digits
Transaction	0 < amt ≤ 1,000,000
Loan	0 < amt ≤ 1,000,000
Balance Cap	≤ 2,000,000,000
💡 Sample Output
text
--- MENU ---
1. Create Account   4. Check Balance
2. Deposit          5. Apply Loan
3. Withdraw         6. Exit

Choose: 2
Enter account number: 100234
Enter deposit amount: 5000
Deposited 5000.0. New balance: 5000.0
🧪 Test Scenarios
ID	Input	Expected
T01	Acc 12ab	"digits only"
T02	Acc 12345	"6-12 digits"
T03	Mobile 98765	"exactly 10 digits"
T04	Deposit -500	"must be positive"
T05	Withdraw > balance	"Insufficient balance"
T06	Balance + deposit > 2e9	"exceed max balance"
🔐 Security
Parameterized SQL (%s)

Credentials in .env (gitignored)

Regex input validation

⚠️ No PIN/auth — see roadmap

🚀 Roadmap
□ PIN login
□ Admin panel
□ Fund transfers
□ Interest calc
□ Transaction history
□ REST API (Flask)
🔗 Links
Docs

Python · MySQL · mysql-connector-python · python-dotenv · PEP 8

Learning

W3Schools MySQL+Python · GeeksforGeeks ACID · Real Python MySQL · Javatpoint Transactions

Tools

VS Code · MySQL Workbench · Regex101 · DB Fiddle

Domain

RBI · Core Banking (Wikipedia)

📜 License
MIT — see LICENSE.

👤 Author
Your Name · GitHub · LinkedIn

⭐ Star this repo if it helped! ⭐

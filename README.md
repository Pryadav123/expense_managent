📊 Expense Management System (Python Desktop App)

A secure, feature-rich expense management desktop application built using Python, Tkinter (ttkbootstrap), and MySQL, designed to help users track, analyze, and manage their expenses efficiently.

🚀 Features
🔐 Authentication

User Signup & Login

Password hashing (SHA-256) for security

Logout functionality with session handling

💸 Expense Management

Add, view, and delete expenses

Each expense includes:

Date

Title

Amount

Category

Notes

User-specific data (multi-user support)

📊 Analytics & Reports

Category-wise expense pie chart

Monthly expense bar chart

Visual analytics using matplotlib

💰 Budget Tracking

Set a monthly budget

Automatic budget exceeded alerts

🔍 Search & Filter

Search expenses by title in real time

Dynamic table refresh

📤 Export

Export expenses to CSV file

Useful for Excel / reports / backups

🎨 UI & UX

Modern themed UI using ttkbootstrap

Clean dashboard layout

Responsive widgets

🛠️ Tech Stack
Layer	Technology
Language	Python
GUI	Tkinter + ttkbootstrap
Database	MySQL
Charts	Matplotlib
Security	hashlib (SHA-256)
📁 Project Structure
expense_manager/
│
├── main.py          # Application entry point
├── auth.py          # Login & Signup logic
├── dashboard.py     # Expense dashboard & features
├── database.py      # MySQL connection
└── README.md        # Project documentation

⚙️ Setup Instructions
1️⃣ Clone the Repository
git clone <your-repo-url>
cd expense_manager

2️⃣ Install Dependencies
pip install mysql-connector-python matplotlib ttkbootstrap

3️⃣ Setup MySQL Database
CREATE DATABASE expense_manager;
USE expense_manager;

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE expenses (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    date DATE,
    title VARCHAR(100),
    amount INT,
    category VARCHAR(50),
    note VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

4️⃣ Update Database Credentials

Edit database.py:

mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="YOUR_PASSWORD",
    database="expense_manager"
)

5️⃣ Run the Application
python main.py
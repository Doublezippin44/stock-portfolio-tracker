# Stock Portfolio Tracker

This is a full-stack web application that allows users to register, log in, and track the real-time value of their stock portfolio. The application features a Python/Flask backend, a MySQL database, and a dynamic frontend built with HTML, CSS, and JavaScript.

## Features
-   User Registration and Login system with password hashing.
-   Ability to record new Buy/Sell transactions from the dashboard.
-   Dynamic dashboard that displays:
    -   The user's real-time total portfolio value.
    -   A donut chart visualizing the portfolio's asset distribution.
    -   A "Popular Stocks" watch list.
-   Interactive candlestick charts in a pop-up modal to view historical performance for any stock.
-   A caching mechanism in the backend to minimize API calls and improve performance.

## Technologies Used
* **Backend:** Python, Flask, Flask-CORS
* **Database:** MySQL
* **Frontend:** HTML, CSS, JavaScript, Tailwind CSS (via CDN), Chart.js, TradingView Lightweight Charts
* **APIs:** Finnhub API for live and historical stock data.

---

## Setup and Installation

This guide will walk you through setting up the project on your local machine.

### 1. Clone the Repository
First, you need to download the project files from GitHub. Open your terminal or command prompt and run:

```bash
git clone [https://github.com/Doublezippin44/stock-portfolio-tracker.git](https://github.com/Doublezippin44/stock-portfolio-tracker.git)
cd stock-portfolio-tracker

2. Install Prerequisites (Software)

You must install Python 3 and a local MySQL server.

Python 3

Ensure you have Python 3 installed. You can download it from python.org.

MySQL Server

This project requires a MySQL server running locally.

On macOS (using Homebrew):

Install Homebrew (if you don't have it): /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

Install MySQL: brew install mysql

Start the MySQL service: brew services start mysql

Run the secure installation to set your 'root' password: mysql_secure_installation

On Windows (using MySQL Installer):

Download and run the MySQL Installer from the official website.

Follow the setup wizard. When prompted, choose the "Server only" or "Developer Default" setup type.

During configuration, you will be asked to create a password for the 'root' user. Remember this password.

Ensure the MySQL server is running as a Windows service.

3. Set Up the Database (SQL)

Log in to your local MySQL server as the root user from your terminal:

Bash
mysql -u root -p
Enter the root password you created during setup.

Copy and paste the following SQL commands to create the database and tables:
CREATE DATABASE stock_portfolio;

USE stock_portfolio;

CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    stock_symbol VARCHAR(10) NOT NULL,
    transaction_type ENUM('BUY', 'SELL') NOT NULL,
    quantity DECIMAL(10, 4) NOT NULL,
    price_per_share DECIMAL(10, 2) NOT NULL,
    transaction_date DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
);

exit;

4. Configure the Project

Install Python Dependencies: In your terminal, from inside the stock-portfolio-tracker folder, run:

On macOS: pip3 install Flask mysql-connector-python flask-cors requests

On Windows: pip install Flask mysql-connector-python flask-cors requests

Add API Keys and Passwords:

Sign up for a free API key at finnhub.io.

Open the app.py file in a text editor.

Find these lines at the top and replace the placeholders with your credentials:

FINNHUB_API_KEY = 'YOUR_FINNHUB_API_KEY_HERE'

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YOUR_DATABASE_PASSWORD_HERE', # <-- The password you set in step 2
    'database': 'stock_portfolio'
}

Running the Application
You must have both the backend server and the frontend file open.

Start the Backend Server: In your terminal, from inside the stock-portfolio-tracker folder, run:

On macOS: python3 app.py

On Windows: python app.py

You should see * Running on http://127.0.0.1:5000

Open the Frontend: Find the login.html file in the project folder and double-click it to open it in your default web browser.

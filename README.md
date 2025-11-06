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

### 1. Prerequisites (Software Installation)
You must install Python 3 and a local MySQL server.

#### Python 3
Ensure you have Python 3 installed. You can download it from [python.org](https://www.python.org/downloads/).

#### MySQL Server
This project requires a MySQL server running locally to store user and transaction data.

**On macOS (using Homebrew):**
1.  Install Homebrew (if you don't have it): `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
2.  Install MySQL: `brew install mysql`
3.  Start the MySQL service: `brew services start mysql`
4.  Run the secure installation to set your 'root' password: `mysql_secure_installation`

**On Windows (using MySQL Installer):**
1.  Download and run the **MySQL Installer** from the [official website](https://dev.mysql.com/downloads/installer/).
2.  Follow the setup wizard. When prompted, choose the **"Server only"** or **"Developer Default"** setup type.
3.  During configuration, you will be asked to create a password for the 'root' user. **Remember this password.**
4.  Ensure the MySQL server is running as a Windows service (it usually starts automatically after installation).

### 2. Database Setup (SQL)
1.  Log in to your local MySQL server as the root user.
    ```bash
    mysql -u root -p
    ```
2.  Enter the root password you created during setup.
3.  Copy and paste the following SQL commands to create the database and tables:
    ```sql
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
    ```

### 3. Project Configuration (API Keys)
1.  Sign up for a free API key at **[finnhub.io](https://finnhub.io)**.
2.  Open the `app.py` file in a text editor.
3.  Find these lines at the top of the file and replace the placeholders with your credentials:
    ```python
    FINNHUB_API_KEY = 'YOUR_FINNHUB_API_KEY_HERE'

    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'YOUR_DATABASE_PASSWORD_HERE', # <-- The password you set in step 1
        'database': 'stock_portfolio'
    }
    ```

### 4. Install Python Dependencies
In your terminal, navigate to the project folder and run the following command to install the required Python libraries:
```bash
pip3 install Flask mysql-connector-python flask-cors requests
Running the Application

You must have both the backend server and the frontend file open.

Start the Backend: In your terminal, from inside the project folder, run the Python server:
python3 app.py
You should see * Running on http://127.0.0.1:5000

Open the Frontend:

On macOS: In a new terminal window, type open login.html.

On Windows: Simply double-click the login.html file to open it in your default web browser.

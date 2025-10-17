# Stock Portfolio Tracker

A full-stack web application that allows users to register, log in, and track the real-time value of their stock portfolio. The application features a Python/Flask backend, a MySQL database, and a dynamic frontend built with HTML, CSS, and JavaScript.

## Features
-   User Registration and Login system with password hashing.
-   Ability to record new Buy/Sell transactions from the dashboard.
-   Dynamic dashboard that displays:
    -   The user's real-time total portfolio value.
    -   A donut chart visualizing the portfolio's asset distribution.
    -   A detailed table of current stock holdings with live market values.
-   A "Popular Stocks" watch list.
-   Interactive candlestick charts in a pop-up modal to view historical performance for any stock.
-   A caching mechanism in the backend to minimize API calls and improve performance.

## Technologies Used
* **Backend:** Python, Flask, Flask-CORS
* **Database:** MySQL
* **Frontend:** HTML, CSS, JavaScript, Tailwind CSS (via CDN), Chart.js, TradingView Lightweight Charts
* **APIs:** Finnhub API for live and historical stock data.

## Setup and Installation

#### 1. Prerequisites
-   Python 3
-   MySQL Server

#### 2. Install Python Dependencies
In your terminal, run the following command to install the required libraries:
```bash
pip3 install Flask mysql-connector-python flask-cors requests

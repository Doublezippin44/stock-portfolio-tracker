from flask import Flask, jsonify, request
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import requests
import time
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# --- NEW: Finnhub API Key ---
FINNHUB_API_KEY = 'd3oln09r01quo6o4ucu0d3oln09r01quo6o4ucug'

db_config = { 'host': 'localhost', 'user': 'root', 'password': 'Project@123', 'database': 'stock_portfolio' }

api_cache = {}
CACHE_DURATION = 120 # 2 minutes

def get_api_data(url):
    now = time.time()
    if url in api_cache and now - api_cache[url]['timestamp'] < CACHE_DURATION:
        return api_cache[url]['data']
    response = requests.get(url)
    data = response.json()
    api_cache[url] = { 'timestamp': now, 'data': data }
    return data

# --- User Management Endpoints (Unchanged) ---
@app.route('/register', methods=['POST'])
def register_user():
    # ... (code is unchanged)
    try:
        data = request.get_json()
        username = data['username']
        email = data['email']
        password = data['password']
        hashed_password = generate_password_hash(password)
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        sql = "INSERT INTO Users (username, email, password_hash) VALUES (%s, %s, %s)"
        values = (username, email, hashed_password)
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['POST'])
def login_user():
    # ... (code is unchanged)
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user and check_password_hash(user['password_hash'], password):
            return jsonify({'message': 'Login successful', 'user_id': user['id']})
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Transactions Endpoint (Unchanged) ---
@app.route('/transactions', methods=['POST'])
def add_transaction():
    # ... (code is unchanged)
    try:
        data = request.get_json()
        user_id = data['user_id']
        stock_symbol = data['stock_symbol']
        transaction_type = data['transaction_type']
        quantity = data['quantity']
        price_per_share = data['price_per_share']
        transaction_date = data['transaction_date']
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        sql = "INSERT INTO Transactions (user_id, stock_symbol, transaction_type, quantity, price_per_share, transaction_date) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (user_id, stock_symbol, transaction_type, quantity, price_per_share, transaction_date)
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Transaction recorded successfully'}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- UPDATED Portfolio and Market Data Endpoints ---
@app.route('/portfolio/<int:user_id>', methods=['GET'])
def get_portfolio(user_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Transactions WHERE user_id = %s", (user_id,))
        transactions = cursor.fetchall()
        cursor.close()
        conn.close()
        holdings = {}
        for trans in transactions:
            symbol = trans['stock_symbol']
            quantity = trans['quantity']
            if trans['transaction_type'] == 'BUY':
                holdings[symbol] = holdings.get(symbol, 0) + quantity
            else:
                holdings[symbol] = holdings.get(symbol, 0) - quantity
        
        portfolio_data = []
        total_portfolio_value = 0
        for symbol, quantity in holdings.items():
            if quantity > 0:
                url = f'https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}'
                data = get_api_data(url)
                
                if 'c' in data and data['c'] != 0:
                    current_price = data['c']
                    market_value = current_price * float(quantity)
                    total_portfolio_value += market_value
                    portfolio_data.append({'stock_symbol': symbol, 'quantity': float(quantity), 'current_price': current_price, 'market_value': market_value})
                else:
                    portfolio_data.append({'stock_symbol': symbol, 'quantity': float(quantity), 'current_price': 'N/A', 'market_value': 'N/A (API Error)'})

        return jsonify({'holdings': portfolio_data, 'total_portfolio_value': total_portfolio_value})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/market-movers', methods=['GET'])
def get_market_movers():
    # Finnhub doesn't have a free top gainers/losers, so we'll use a static list of popular stocks
    popular_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META']
    return jsonify({'popular_stocks': popular_stocks})

@app.route('/api/stock-data/<string:symbol>', methods=['GET'])
def get_stock_data(symbol):
    try:
        # Get historical data for the last year for the candlestick chart
        today = datetime.now()
        one_year_ago = today - timedelta(days=365)
        
        from_timestamp = int(one_year_ago.timestamp())
        to_timestamp = int(today.timestamp())

        url = f'https://finnhub.io/api/v1/stock/candle?symbol={symbol}&resolution=D&from={from_timestamp}&to={to_timestamp}&token={FINNHUB_API_KEY}'
        data = get_api_data(url)
        
        # Transform Finnhub data to the format our chart expects
        if data.get('s') == 'ok':
            chart_data = []
            for i in range(len(data['t'])):
                chart_data.append({
                    "time": data['t'][i],
                    "open": data['o'][i],
                    "high": data['h'][i],
                    "low": data['l'][i],
                    "close": data['c'][i]
                })
            return jsonify({'chart_data': chart_data})
        else:
            return jsonify({'error': 'Could not retrieve chart data from API.'}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

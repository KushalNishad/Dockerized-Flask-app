from flask import Flask, render_template, request, jsonify, redirect, url_for
import pymysql
import matplotlib.pyplot as plt
import os
from database.db_config import get_db_connection

app = Flask(__name__)

# --- Home (Now direct dashboard) ---
@app.route('/')
def home():
    return redirect(url_for('dashboard'))

# --- Dashboard (No login required) ---
@app.route('/dashboard')
def dashboard():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT user_name, amount FROM transactions ORDER BY transaction_date DESC LIMIT 10")
    transactions = cursor.fetchall()
    connection.close()

    # Prepare data for chart
    users = [row[0] for row in transactions]
    amounts = [float(row[1]) for row in transactions]

    # Create chart
    plt.figure(figsize=(8, 4))
    plt.bar(users, amounts, color='skyblue')
    plt.title('Latest Transactions')
    plt.xlabel('User')
    plt.ylabel('Amount')
    plt.xticks(rotation=45)
    chart_path = os.path.join('static', 'chart.png')
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()

    return render_template('dashboard.html', transactions=transactions, chart='chart.png')

# --- Create DB Table ---
@app.route('/create_table', methods=['GET'])
def create_table():
    connection = get_db_connection()
    cursor = connection.cursor()
    create_table_query = """
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_name VARCHAR(255) NOT NULL,
            amount DECIMAL(10, 2) NOT NULL,
            transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    cursor.execute(create_table_query)
    connection.commit()
    connection.close()
    return "Table created successfully!"

# --- Add Transaction ---
@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    user_name = request.form['user_name']
    amount = request.form['amount']

    connection = get_db_connection()
    cursor = connection.cursor()
    insert_query = """
        INSERT INTO transactions (user_name, amount) 
        VALUES (%s, %s)
    """
    cursor.execute(insert_query, (user_name, amount))
    connection.commit()
    connection.close()
    return redirect(url_for('dashboard'))

# --- API to list all transactions ---
@app.route('/transactions', methods=['GET'])
def transactions():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM transactions ORDER BY transaction_date DESC")
    result = cursor.fetchall()
    connection.close()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

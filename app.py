from flask import Flask, render_template, request, jsonify
from database.db_config import get_db_connection

app = Flask(__name__)

@app.route('/')
def index():
   
    #connection = get_db_connection()
    #cursor = connection.cursor()
    #cursor.execute("""
     #   SELECT user_name, SUM(amount) AS total_spent
      # GROUP BY user_name
       # ORDER BY total_spent DESC
        #LIMIT 5
    #""")
    #friends = cursor.fetchall()
    #connection.close()

    friends = [
        {'user_name': 'Krupal', 'item':'Shaadi', 'total_spent': 50000},
        {'user_name': 'Karan', 'item':'Marshall', 'total_spent': 700},
        {'user_name': 'Naynesh', 'item':'Hookah', 'total_spent': 500},
        {'user_name': 'Tanmay', 'item':'Hookah', 'total_spent': 400},
        {'user_name': 'Heer', 'item':'Picnic', 'total_spent': 150},
    ]

    return render_template('index.html', friends=friends)

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
    return "Transaction added successfully!"

@app.route('/transactions', methods=['GET'])
def transactions():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM transactions ORDER BY transaction_date DESC")
    result = cursor.fetchall()
    connection.close()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)

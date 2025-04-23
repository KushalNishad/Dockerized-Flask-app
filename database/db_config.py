import pymysql

def get_db_connection():
    connection = pymysql.connect(
        host='mydb.c98a60agsfko.us-east-2.rds.amazonaws.com',  # AWS RDS Endpoint
        user='flask',        # Replace with your RDS username
        password='flask_pass',  # Replace with your RDS password
        db='devprojdb',       # Replace with your database name
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

import pymysql

def get_db_connection():
    connection = pymysql.connect(
        host='mydb.cylck8yh5jkc.eu-central-1.rds.amazonaws.com',  # AWS RDS Endpoint
        user='dbuser',        # Replace with your RDS username
        password='dbpassword',  # Replace with your RDS password
        db='devprojdb',       # Replace with your database name
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

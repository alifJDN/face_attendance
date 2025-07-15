import mysql.connector
from mysql.connector import Error

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'attendance_logger'
}

def connect_sql():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print('MySQL successfully connected')
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def insert_data(name):
    define_connection = connect_sql()
    if define_connection is None:
        print("Failed to connect to database, cannot insert data")
        return
    
    cursor = define_connection.cursor()
    if not name or name.lower() == "unknown":  # Simplified check
        name = "unknown"  # Fix typo
    
    insert_query = """
    INSERT INTO attendances (name) VALUES (%s);
    """
    
    try:
        input_data = (name,)
        cursor.execute(insert_query, input_data)
        define_connection.commit()
        print(f"Input success: {name}")
    except Error as e:
        print(f"Error inserting data: {e}")
        define_connection.rollback()
    finally:
        cursor.close()
        define_connection.close()
        print("Database connection closed")
import mysql
from mysql.connector import Error
import mysql.connector

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
            print('mysql successfully connected')
            return connection
        
    except Error as e:
        print(f"error: {e}")


def insert_data(name):
    define_connection = connect_sql()
    cursor = define_connection.cursor()
    if len(name) == 0 or name == "unknown":
        name = ("unkown")
    insert_query = """
    INSERT INTO attendances (name) VALUES (%s);
    """
    try:
        input_data = (name,)
        cursor.execute(insert_query,input_data)
        define_connection.commit()
        print("input success")
    except Error as e:
        print(f"Error: {e}")


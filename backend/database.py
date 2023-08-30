import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import errorcode


load_dotenv()  

config = {
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST'),
    'database': os.environ.get('DB_DATABASE'),
    'raise_on_warnings': True
}

def init_db():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            )
        """)
        connection.commit()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    finally:
        cursor.close()
        connection.close()

def insert_user(name, email, password):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        connection.commit()
        success = True
    except mysql.connector.IntegrityError:
        success = False  
    finally:
        cursor.close()
        connection.close()
    return success

init_db()  

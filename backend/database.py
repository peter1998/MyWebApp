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

def get_user_by_email(email):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user_data = cursor.fetchone()
        return user_data
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        cursor.close()
        connection.close()

def update_user(email, name=None, password=None):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        update_query = "UPDATE users SET "
        params = []
        
        if name:
            update_query += "name=%s,"
            params.append(name)
        if password:
            update_query += "password=%s,"
            params.append(password)

        update_query = update_query.rstrip(',')
        update_query += " WHERE email=%s"
        params.append(email)
        
        cursor.execute(update_query, params)
        connection.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    finally:
        cursor.close()
        connection.close()

def delete_user(email):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM users WHERE email = %s", (email,))
        connection.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    finally:
        cursor.close()
        connection.close()


init_db()

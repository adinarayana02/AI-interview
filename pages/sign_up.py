import mysql.connector
from mysql.connector import Error
import hashlib

# Database connection function
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Thot@adi2002",
            database="interview_system"
        )
        return connection
    except Error as e:
        raise ConnectionError(f"Error: {e}")

# Hashing password for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Sign Up function
def sign_up(username, email, password, company_name):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        hashed_password = hash_password(password)
        query = "INSERT INTO recruiter (company_name, email, username, password) VALUES (%s, %s, %s, %s)"
        values = (company_name, email, username, hashed_password)
        cursor.execute(query, values)
        connection.commit()
        return "Sign Up Successful! You can now log in."
    except Error as e:
        return f"Error: {e}"
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

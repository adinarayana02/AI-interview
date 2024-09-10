import streamlit as st
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
        st.error(f"Database connection error: {e}")
        return None

# Hashing password for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Log In function
def log_in(username, password):
    connection = get_db_connection()
    if connection is None:
        return "Failed to connect to the database."
    
    try:
        cursor = connection.cursor()
        hashed_password = hash_password(password)
        query = """
        SELECT * FROM recruiter WHERE username = %s AND password = %s
        """
        values = (username, hashed_password)
        cursor.execute(query, values)
        result = cursor.fetchone()
        if result:
            return "Login Successful!"
        else:
            return "Invalid username or password."
    except Error as e:
        return f"Error: {e}"
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# Streamlit Login Page
def login_page():
    st.title("Recruiter Log In")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Log In"):
        if username and password:
            message = log_in(username, password)
            if "Successful" in message:
                st.success(message)
                st.session_state.logged_in = True
                st.experimental_rerun()  # Refresh the page to redirect
            else:
                st.error(message)
        else:
            st.error("Please fill in all fields.")

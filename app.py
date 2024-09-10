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
            password="Thot@adi2002",  # Replace with your MySQL password
            database="interview_system"
        )
        return connection
    except Error as e:
        st.error(f"Database connection error: {e}")
        return None

# Hashing password for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Sign Up function
def sign_up(username, email, password, company_name):
    connection = get_db_connection()
    if connection is None:
        return "Failed to connect to the database."
    
    try:
        cursor = connection.cursor()
        # Prepare the INSERT query
        query = """
        INSERT INTO recruiter (company_name, email, username, password) 
        VALUES (%s, %s, %s, %s)
        """
        values = (company_name, email, username, hash_password(password))
        cursor.execute(query, values)
        connection.commit()
        return "Sign Up Successful! You can now log in."
    except Error as e:
        return f"Error: {e}"
    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()

# Streamlit Sign Up Page
def sign_up_page():
    st.title("Recruiter Sign Up")
    company_name = st.text_input("Company Name")
    email = st.text_input("Email")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Sign Up"):
        if company_name and email and username and password:
            message = sign_up(username, email, password, company_name)
            if "Successful" in message:
                st.success(message)
            else:
                st.error(message)
        else:
            st.error("Please fill in all fields.")

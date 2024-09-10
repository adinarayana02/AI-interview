import streamlit as st
import mysql.connector
from mysql.connector import Error
import hashlib

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Thot@adi2002",
        database="interview_system"
    )

# Hashing password for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Sign Up function
def sign_up(company_name, username, email, password):
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
        if connection.is_connected():
            cursor.close()
            connection.close()

# Streamlit App Layout for Sign Up
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

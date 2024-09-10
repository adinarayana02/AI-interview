import streamlit as st
import mysql.connector
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get the Fernet key from environment variables
fernet_key = os.getenv('FERNET_KEY')
if fernet_key:
    fernet = Fernet(fernet_key.encode())
else:
    st.error("Fernet key is not set in environment variables.")

def encrypt_password(password):
    return fernet.encrypt(password.encode()).decode()

def signup_page():
    st.title("Sign Up")

    with st.form(key='signup_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        email = st.text_input("Email")
        submit_button = st.form_submit_button(label='Sign Up')

        if submit_button:
            if username and password and email:
                encrypted_password = encrypt_password(password)
                try:
                    connection = mysql.connector.connect(
                        host=os.getenv('DB_HOST'),
                        user=os.getenv('DB_USER'),
                        password=os.getenv('DB_PASSWORD'),
                        database=os.getenv('DB_NAME')
                    )
                    cursor = connection.cursor()
                    cursor.execute('''
                        INSERT INTO users (username, password, email)
                        VALUES (%s, %s, %s)
                    ''', (username, encrypted_password, email))
                    connection.commit()
                    cursor.close()
                    connection.close()
                    st.success("Sign Up successful!")
                except mysql.connector.Error as err:
                    st.error(f"Database error: {err}")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.error("Please fill in all fields.")

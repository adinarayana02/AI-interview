import streamlit as st
import mysql.connector
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Setup encryption
fernet_key = os.getenv('FERNET_KEY').encode()
if not fernet_key:
    st.error("Fernet key not set in environment variables.")
else:
    fernet = Fernet(fernet_key)

def decrypt_password(encrypted_password):
    return fernet.decrypt(encrypted_password.encode()).decode()

def login_page():
    st.title("Log In")

    with st.form(key='login_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button(label='Log In')

        if submit_button:
            if username and password:
                connection = mysql.connector.connect(
                    host=os.getenv('DB_HOST'),
                    user=os.getenv('DB_USER'),
                    password=os.getenv('DB_PASSWORD'),
                    database=os.getenv('DB_NAME')
                )
                cursor = connection.cursor()
                cursor.execute('''
                    SELECT password FROM users WHERE username = %s
                ''', (username,))
                result = cursor.fetchone()
                if result:
                    stored_password = result[0]
                    if decrypt_password(stored_password) == password:
                        st.success("Log In successful!")
                    else:
                        st.error("Invalid username or password.")
                else:
                    st.error("User not found.")
                cursor.close()
                connection.close()
            else:
                st.error("Please fill in all fields.")

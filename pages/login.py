import streamlit as st
import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def login_page():
    st.title("Log In")

    with st.form(key='login_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button(label='Log In')

        if submit_button:
            if username and password:
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Thot@adi2002",
                    database="interview_system"
                )
                cursor = connection.cursor()
                cursor.execute('''
                    SELECT password FROM users WHERE username = %s
                ''', (username,))
                result = cursor.fetchone()
                if result:
                    stored_password = result[0]
                    if stored_password == password:
                        st.success("Log In successful!")
                    else:
                        st.error("Invalid username or password.")
                else:
                    st.error("User not found.")
                cursor.close()
                connection.close()
            else:
                st.error("Please fill in all fields.")

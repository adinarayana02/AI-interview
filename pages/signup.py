import streamlit as st
import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def signup_page():
    st.title("Recruiter Sign Up")

    with st.form(key='signup_form'):
        company_name = st.text_input("Company Name")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        email = st.text_input("Email")
        submit_button = st.form_submit_button(label='Sign Up')

        if submit_button:
            if company_name and username and password and email:
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Thot@adi2002",
                    database="interview_system"
                )
                cursor = connection.cursor()
                cursor.execute('''
                    INSERT INTO recruiter (company_name, username, password, email)
                    VALUES (%s, %s, %s, %s)
                ''', (company_name, username, password, email))
                connection.commit()
                cursor.close()
                connection.close()
                st.success("Sign Up successful!")
            else:
                st.error("Please fill in all fields.")

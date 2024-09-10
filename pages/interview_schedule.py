import streamlit as st
import mysql.connector
import openai
from dotenv import load_dotenv
import os
import PyPDF2
from cryptography.fernet import Fernet
from io import BytesIO
from random import choice
import string

# Load environment variables
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Thot@adi2002",
        database="interview_system"
    )

# Function to generate a random password
def generate_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(choice(characters) for i in range(length))

# Function to extract email and name from resume
def extract_email_and_name_from_resume(resume_path):
    # Dummy implementation - replace with actual logic
    email = "example@example.com"
    name = "John Doe"
    return email, name

# Function to create interview schedule
def create_interview_schedule(recruiter_id, job_title, job_description, job_requirements, candidate_resume, experience, no_of_questions, questions):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    email, name = extract_email_and_name_from_resume(candidate_resume)
    candidate_username = email
    candidate_password = generate_password()

    cursor.execute('''
        INSERT INTO interview_schedule (recruiter_id, job_title, job_description, job_requirements, candidate_resume, experience, no_of_questions, questions)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (recruiter_id, job_title, job_description, job_requirements, candidate_resume, experience, no_of_questions, questions))

    schedule_id = cursor.lastrowid

    cursor.execute('''
        INSERT INTO candidate (candidate_username, candidate_password, schedule_id)
        VALUES (%s, %s, %s)
    ''', (candidate_username, candidate_password, schedule_id))

    connection.commit()
    cursor.close()
    connection.close()

    return candidate_username, candidate_password

# Streamlit UI
def main():
    st.title('AI Interview System')

    menu = ["Recruiter", "Candidate"]
    choice = st.sidebar.selectbox("Select Role", menu)

    if choice == "Recruiter":
        st.subheader("Recruiter Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        if st.button("Login"):
            # Authentication logic here
            st.success("Logged in successfully")

        st.subheader("Create Interview Schedule")
        job_title = st.text_input("Job Title")
        job_description = st.text_area("Job Description")
        job_requirements = st.text_area("Job Requirements")
        candidate_resume = st.file_uploader("Upload Resume", type=["pdf"])
        experience = st.number_input("Experience (years)", min_value=0)
        no_of_questions = st.number_input("Number of Questions", min_value=1)
        questions = st.file_uploader("Upload Questions", type=["txt"])

        if st.button("Create Interview Schedule"):
            if candidate_resume and questions:
                candidate_username, candidate_password = create_interview_schedule(
                    recruiter_id=1,  # Replace with actual recruiter ID
                    job_title=job_title,
                    job_description=job_description,
                    job_requirements=job_requirements,
                    candidate_resume=candidate_resume,
                    experience=experience,
                    no_of_questions=no_of_questions,
                    questions=questions.read()
                )
                st.success(f"Interview schedule created successfully.\nUsername: {candidate_username}\nPassword: {candidate_password}")
            else:
                st.error("Please upload both resume and questions.")

    elif choice == "Candidate":
        st.subheader("Candidate Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        if st.button("Login"):
            # Authentication logic here
            st.success("Logged in successfully")

        st.subheader("Start Interview")
        # Assuming the interview questions and other details are available
        st.write("Interview Questions will be displayed here.")

if __name__ == "__main__":
    main()

import streamlit as st
import mysql.connector
import openai
import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from PyPDF2 import PdfFileReader

# Load environment variables
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Setup encryption
fernet_key = os.getenv('FERNET_KEY').encode()
fernet = Fernet(fernet_key)

def encrypt_password(password):
    return fernet.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    return fernet.decrypt(encrypted_password.encode()).decode()

def extract_email_and_name_from_resume(resume_content):
    # Dummy implementation - replace with actual logic using OpenAI
    return "example@example.com", "John Doe"

def create_interview_schedule(recruiter_id, job_title, job_description, job_requirements, candidate_resume, experience, no_of_questions, questions):
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    cursor = connection.cursor()

    email, name = extract_email_and_name_from_resume(candidate_resume)

    candidate_username = email
    candidate_password = encrypt_password("user@123")

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

    return candidate_username, "user@123"

def interview_schedule_page():
    st.title("Create Interview Schedule")

    with st.form(key='interview_schedule_form'):
        recruiter_id = st.text_input("Recruiter ID")
        job_title = st.text_input("Job Title")
        job_description = st.text_area("Job Description")
        job_requirements = st.text_area("Job Requirements")
        candidate_resume = st.file_uploader("Upload Resume", type=["pdf"])
        experience = st.text_input("Experience Level")
        no_of_questions = st.number_input("Number of Questions", min_value=1)
        questions = st.text_area("Interview Questions")
        
        submit_button = st.form_submit_button(label='Create Schedule')
        if submit_button:
            if candidate_resume:
                candidate_resume_content = candidate_resume.read()
                username, password = create_interview_schedule(
                    recruiter_id, job_title, job_description, job_requirements, candidate_resume_content, experience, no_of_questions, questions
                )
                st.success("Interview schedule created successfully!")
                st.write(f"Candidate Username: {username}")
                st.write(f"Candidate Password: {password}")
            else:
                st.error("Please upload a resume.")

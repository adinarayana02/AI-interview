import streamlit as st
import mysql.connector
import os
from dotenv import load_dotenv
from PyPDF2 import PdfFileReader

# Load environment variables
load_dotenv()

def extract_email_and_name_from_resume(resume):
    # Dummy implementation - replace with actual logic
    with PdfFileReader(resume) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        # Simple example of extracting email (replace with actual extraction logic)
        email = "example@example.com"  # Placeholder email extraction
        name = "John Doe"  # Placeholder name extraction
    return email, name

def create_interview_schedule(recruiter_id, job_title, job_description, job_requirements, candidate_resume, experience, no_of_questions, questions):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Thot@adi2002",
        database="interview_system"
    )
    cursor = connection.cursor()

    email, name = extract_email_and_name_from_resume(candidate_resume)

    candidate_username = email
    candidate_password = "user@123"

    cursor.execute('''
        INSERT INTO interview_schedule (recruiter_id, job_title, job_description, job_requirements, candidate_resume, experience, no_of_questions, questions)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (recruiter_id, job_title, job_description, job_requirements, candidate_resume.name, experience, no_of_questions, questions))

    schedule_id = cursor.lastrowid

    cursor.execute('''
        INSERT INTO interview_credentials (schedule_id, username, password)
        VALUES (%s, %s, %s)
    ''', (schedule_id, candidate_username, candidate_password))

    connection.commit()
    cursor.close()
    connection.close()

    return candidate_username, candidate_password

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
                username, password = create_interview_schedule(
                    recruiter_id, job_title, job_description, job_requirements, candidate_resume, experience, no_of_questions, questions
                )
                st.success("Interview schedule created successfully!")
                st.write(f"Candidate Username: {username}")
                st.write(f"Candidate Password: {password}")
            else:
                st.error("Please upload a resume.")

import streamlit as st
import mysql.connector
import os

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Thot@adi2002",
        database="interview_system"
    )

# Function to create interview schedule
def create_interview_schedule(recruiter_id, job_title, job_description, job_requirements, candidate_resume, experience, no_of_questions, questions):
    connection = get_db_connection()
    cursor = connection.cursor()

    candidate_username = "extracted_email@example.com"  # Replace with actual extraction logic
    candidate_password = "user@123"

    cursor.execute('''
        INSERT INTO interview_schedule (recruiter_id, job_title, job_description, job_requirements, candidate_resume, experience, no_of_questions, questions)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (recruiter_id, job_title, job_description, job_requirements, candidate_resume, experience, no_of_questions, questions))

    schedule_id = cursor.lastrowid

    cursor.execute('''
        INSERT INTO interview_credentials (schedule_id, username, password)
        VALUES (%s, %s, %s)
    ''', (schedule_id, candidate_username, candidate_password))

    connection.commit()
    cursor.close()
    connection.close()

    return candidate_username, candidate_password

# Streamlit App Layout
def interview_schedule_page():
    st.title("Create Interview Schedule")

    with st.form(key='interview_schedule_form'):
        recruiter_id = st.text_input("Recruiter ID")
        job_title = st.text_input("Job Title")
        job_description = st.text_area("Job Description")
        job_requirements = st.text_area("Job Requirements")
        candidate_resume = st.text_input("Resume File Path")
        experience = st.text_input("Experience Level")
        no_of_questions = st.number_input("Number of Questions", min_value=1)
        questions = st.text_area("Interview Questions")
        
        submit_button = st.form_submit_button(label='Create Schedule')
        if submit_button:
            if recruiter_id and job_title and job_description and job_requirements and candidate_resume and experience and no_of_questions and questions:
                username, password = create_interview_schedule(
                    recruiter_id, job_title, job_description, job_requirements, candidate_resume, experience, no_of_questions, questions
                )
                st.success("Interview schedule created successfully!")
                st.write(f"Candidate Username: {username}")
                st.write(f"Candidate Password: {password}")
            else:
                st.error("Please fill in all fields.")

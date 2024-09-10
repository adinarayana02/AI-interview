import streamlit as st
import openai
import PyPDF2
import mysql.connector
from mysql.connector import Error

from secrets import token_hex


# Function to extract email and name from resume using OpenAI
def extract_email_and_name_from_resume(pdf_file):
    openai.api_key = st.secrets["openai"]["api_key"]
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    resume_text = ""
    for page in pdf_reader.pages:
        resume_text += page.extract_text()

    # Using OpenAI API to extract email and name
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Extract the email and name from the following text:\n\n{resume_text}",
        max_tokens=100
    )

    # Assuming response is in the format: "Email: example@example.com, Name: John Doe"
    result = response.choices[0].text.strip()
    email = result.split('Email: ')[1].split(',')[0].strip()
    name = result.split('Name: ')[1].strip()
    return email, name


# Function to create interview schedule
def create_interview_schedule(recruiter_id, job_title, job_description, job_requirements, candidate_resume, experience,
                              no_of_questions, questions):
    email, name = extract_email_and_name_from_resume(candidate_resume)
    candidate_username = email
    candidate_password = token_hex(8)  # Generating a random password

    try:
        # Connect to MySQL
        connection = mysql.connector.connect(
            host='localhost',
            database='interview_system',
            user='root',
            password='Thot@adi2002'
        )
        if connection.is_connected():
            cursor = connection.cursor()

            # Insert into interview_schedule table
            cursor.execute('''
                INSERT INTO interview_schedule (recruiter_id, job_title, job_description, job_requirements, candidate_resume, experience, no_of_questions, questions)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (recruiter_id, job_title, job_description, job_requirements, candidate_resume.name, experience,
                  no_of_questions, questions))
            schedule_id = cursor.lastrowid

            # Insert into candidate table
            cursor.execute('''
                INSERT INTO candidate (candidate_username, candidate_password, schedule_id)
                VALUES (%s, %s, %s)
            ''', (candidate_username, candidate_password, schedule_id))

            # Insert into interview_credentials table
            cursor.execute('''
                INSERT INTO interview_credentials (schedule_id, candidate_username, candidate_password)
                VALUES (%s, %s, %s)
            ''', (schedule_id, candidate_username, candidate_password))

            connection.commit()
            return "Interview schedule created successfully!"
    except Error as e:
        return f"Error: {str(e)}"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# Streamlit page for interview scheduling
def interview_schedule_page():
    st.header("Create Interview Schedule")

    recruiter_id = st.number_input("Recruiter ID", min_value=1)
    job_title = st.text_input("Job Title")
    job_description = st.text_area("Job Description")
    job_requirements = st.text_area("Job Requirements")
    candidate_resume = st.file_uploader("Upload Candidate Resume (PDF)", type="pdf")
    experience = st.number_input("Experience (in years)", min_value=0)
    no_of_questions = st.number_input("Number of Questions", min_value=1)
    questions = st.text_area("Questions")

    if st.button("Create Interview Schedule"):
        if candidate_resume:
            message = create_interview_schedule(recruiter_id, job_title, job_description, job_requirements,
                                                candidate_resume, experience, no_of_questions, questions)
            st.success(message)
        else:
            st.error("Please upload the candidate resume.")

# app.py

import streamlit as st
from pages.signup import signup_page
from pages.login import login_page
from pages.interview_schedule import interview_schedule_page
from pages.interview import interview_page

def main():
    st.sidebar.title("AI Interview System")
    page = st.sidebar.selectbox("Choose a page", ["Sign Up", "Log In", "Interview Schedule", "Interview"])

    if page == "Sign Up":
        signup_page()
    elif page == "Log In":
        login_page()
    elif page == "Interview Schedule":
        interview_schedule_page()
    elif page == "Interview":
        interview_page()

if __name__ == "__main__":
    main()

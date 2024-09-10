import streamlit as st
from pages.signup import signup_page
from pages.login import login_page
from pages.interview_schedule import interview_schedule_page

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Select a page", ["Sign Up", "Log In", "Create Interview Schedule"])

    if page == "Sign Up":
        signup_page()
    elif page == "Log In":
        login_page()
    elif page == "Create Interview Schedule":
        interview_schedule_page()

if __name__ == "__main__":
    main()

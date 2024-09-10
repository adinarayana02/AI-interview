import streamlit as st

from pages.login import login_page
from pages.interview_schedule import interview_schedule_page

def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", ["Sign Up", "Log In", "Create Interview Schedule"])

    if selection == "Sign Up":
        signup_page()
    elif selection == "Log In":
        login_page()
    elif selection == "Create Interview Schedule":
        interview_schedule_page()

if __name__ == "__main__":
    main()

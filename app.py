import streamlit as st
from pages.login import login_page
from pages.interview_schedule import interview_schedule_page

def main():
    st.sidebar.title("Navigation")

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        interview_schedule_page()
    else:
        page = st.sidebar.radio("Go to", ["Log In", "Sign Up"])
        if page == "Log In":
            login_page()
        elif page == "Sign Up":
            sign_up_page()

if __name__ == "__main__":
    main()

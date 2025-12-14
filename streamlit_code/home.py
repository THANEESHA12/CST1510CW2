import streamlit as st
import RegisterPage
import LogInPage #Importing all the functions here so as to be able to create a connection
import cybersecurity
import data_science
import it_operations
import AI_analyzer          
import gemini_api_streamlit 

def home_page():
    st.set_page_config(page_title="Multi-Domain Intelligence Platform", layout="wide")

    #Keeps track on what page is currently on
    if "current_page" not in st.session_state:
        st.session_state.current_page = "home"

    #This sidebar contains information of what this platform is consists of
    with st.sidebar:
        st.title("Navigation")
        st.divider()
        st.markdown("**This platform contains:**")
        st.write("1. Cybersecurity")
        st.write("2. Data Science")
        st.write("3. IT Operations")
        st.write("4. AI Analyzer")
        st.write("5. AI Assistant")
        st.divider()
        st.write("Each domain has a database, analytics charts, and crud operations.")

    
    #Printing a title that demonstrate the Multi-Domain platform
    st.title("**MULTI-DOMAIN INTELLIGENCE PLATFORM**")
    st.divider()

    # If user press on the register button the register page will open and if user press on the log in button the log in page will open
    if st.session_state.current_page == "home":
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### New User?")
            if st.button("Register", use_container_width=True, key="home_register_btn"):
                st.session_state.current_page = "register"
                st.rerun()
        with col2:
            st.markdown("### Existing User?")
            if st.button("Log In", use_container_width=True, key="home_login_btn"):
                st.session_state.current_page = "login"
                st.rerun()

    #If the user is on register the register_page() is called from the RegisterPage.py and the others follows the same logic
    elif st.session_state.current_page == "register":
        RegisterPage.register_page()

    elif st.session_state.current_page == "login":
        LogInPage.login_page()

    elif st.session_state.current_page == "cybersecurity":
        cybersecurity.cybersecurity_main()

    elif st.session_state.current_page == "data_science":
        data_science.data_science_main()

    elif st.session_state.current_page == "it_operations":
        it_operations.itoperations_main()

    elif st.session_state.current_page == "AI_analyzer":   
        AI_analyzer.ai_analyzer_main()

    elif st.session_state.current_page == "gemini_api_streamlit":        
        gemini_api_streamlit.gemini_main()

if __name__ == "__main__":
    home_page()

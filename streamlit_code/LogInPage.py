import streamlit as st
import os
import sys

def login_page():
    # Adding the path so that the function from the auth.py can be imported
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    try:
        #Calling the login_user function from auth
        from auth import login_user
    except ImportError as error:
        st.error(f"Error importing auth: {error}") #An error message is displayed if imported is unsuccessful
        return
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("**LOG IN PAGE**") #Displaying the title of the page
        st.divider()

    st.set_page_config(page_title="Login", layout="wide")


    #Centering the form to fill out in the middle 
    left_space, center_col, right_space = st.columns([1, 2, 1])
    with center_col:
        with st.container():
            #Domain can be chosen from to log in into using the username and password
            domain = st.selectbox("Select Domain", ["Cyber Security", "Data Science", "IT Operations"], key="login_domain")
            username = st.text_input("Username", placeholder="Enter your username", key="login_username")
            password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
            role = st.selectbox("Select Role", ["user", "analyst", "manager"], key="login_role") #Role can be chosen as to how someone wants to be registered as

            st.divider()
            
            #Cnetering the log in button in the middle
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                login_btn = st.button("LOGIN", use_container_width=True, key="login_submit")

            if login_btn:
                if not username or not password:
                    st.error("Please fill in all required fields") #A message is displayed if the password and username field is not filled
                else:
                    try:
                        success = login_user(username, password) #If a user have registered they will be abke to log in
                        if success:
                            st.success("Login successful!")
                            st.success(f"Welcome back, {username}!")

                            # Set session info
                            st.session_state.user_logged_in = True
                            st.session_state.username = username
                            st.session_state.user_role = role

                            # Route to chosen domain
                            if domain == "Cyber Security":
                                st.session_state.current_page = "cybersecurity"
                            elif domain == "Data Science":
                                st.session_state.current_page = "data_science"
                            elif domain == "IT Operations":
                                st.session_state.current_page = "it_operations"
                            st.rerun()
                        else:
                            st.error("Login failed! Check your username and password.") #If account is not registered a failed login message will be displayed therefore from there itself user can press the create new account to be able to register
                    except Exception as error:
                        st.error(f"Login error: {error}")

        col_left, col_right = st.columns(2)
        with col_left:
            #The back to home is directed to the home page
            if st.button("Back to Home", use_container_width=True, key="login_back_home"):
                st.session_state.current_page = "home"
                st.rerun()
        with col_right:
            #The create new account button is directed to the register so as to be able to register account
            if st.button("Create New Account", use_container_width=True, key="login_to_register"):
                st.session_state.current_page = "register"
                st.rerun()

if __name__ == "__main__":
    login_page()

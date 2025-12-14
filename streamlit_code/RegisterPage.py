import streamlit as st
import os
import sys

def register_page():
    # Adding path to be able to import form auth.py
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    try:
        #Calling functions from auth
        from auth import register_user, validate_username, validate_password, check_password_strength
    except ImportError as error:
        st.error(f"Error importing auth: {error}") #An error message is displayed if the import was unsuccessful
        return

    st.set_page_config(page_title="Register", layout="wide")

    # Centering the title in the middle
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("**REGISTER PAGE**") #Displaying the name of the page
        st.divider()

        st.subheader("Create New Account")


        #Domain can be chosen from to register into and then will be directed to that domain
        domain = st.selectbox("Select Domain", ["Cyber Security", "Data Science", "IT Operations"], key="reg_domain")
        username = st.text_input("Username", placeholder="Enter username (min 5 characters)", key="reg_username")
        password = st.text_input("Password", type="password", placeholder="Enter password", key="reg_password")

        #Checks if the password entered is strong , medium or weak
        if password:
            strength = check_password_strength(password)
            if strength == "Weak":
                st.warning(f"Password Strength: {strength}")
            elif strength == "Medium":
                st.info(f"Password Strength: {strength}")
            else:
                st.success(f"Password Strength: {strength}")
         
         #Confirming password to allow registration
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm Password", key="reg_confirm")
        role = st.selectbox("Select Role", ["user", "analyst", "manager"], key="reg_role") #Role can be chosen to register

        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            submit = st.button("SUBMIT", use_container_width=True, key="reg_submit") #When the submit button is pressed the user will be directed to the domain they have chosen

        if submit:
            if not all([username, password, confirm_password]):
                st.error("Please fill in all fields") #An error is displayed if these field are left unfilled
            elif password != confirm_password:
                st.error("Passwords do not match")
            else:
                is_valid_username, username_error = validate_username(username)
                is_valid_password, password_errors = validate_password(password)

                if not is_valid_username:
                    st.error(f"Username error: {username_error}")
                if not is_valid_password:
                    st.error("Password errors:") #Wrong password entered
                    for err in password_errors:
                        st.error(f"- {err}")

                if is_valid_username and is_valid_password:
                    try:
                        auth_role = "admin" if role == "manager" else role
                        success = register_user(username, password, auth_role)
                        if success:
                            st.success("Registration successful!")
                            st.success(f"Welcome {username}! You are registered as {role} for {domain} domain")

                            # Set session info
                            st.session_state.user_logged_in = True
                            st.session_state.username = username
                            st.session_state.user_role = role

                            # Navigate directly to the chosen domain
                            if domain == "Cyber Security":
                                st.session_state.current_page = "cybersecurity"
                            elif domain == "Data Science":
                                st.session_state.current_page = "data_science"
                            elif domain == "IT Operations":
                                st.session_state.current_page = "it_operations"
                            st.rerun()
                        else:
                            st.error("Registration failed. Username may already exist.") #This message is displayed if username has already been registered in
                    except Exception as error:
                        st.error(f"Registration error: {error}")

        b1, b2, b3 = st.columns([1, 1, 1])
        with b2:
            if st.button("Back to Home", use_container_width=True, key="reg_back_home"):
                st.session_state.current_page = "home"
                st.rerun()

if __name__ == "__main__":
    register_page()

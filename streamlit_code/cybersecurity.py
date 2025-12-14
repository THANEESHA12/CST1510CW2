import streamlit as st
import pandas as pd
import plotly.express as px
import os, sys #Using this for file path

#Adding the parent directory so that importing from an outside folder is possible
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#Importing the crud operations from incidents.py
from app.data.incidents import get_all_incidents, insert_incident, update_incident_status, delete_incident

def cybersecurity_main():
    st.set_page_config(page_title="Cyber Security", layout="wide")
    st.session_state.show_register = False
    st.session_state.show_login = False

    st.title("**CYBERSECURITY DASHBOARD**") #A title displaying the cybersecurity dashboard
    st.divider()

    # Sidebar navigation that gives access to other domains and the AI assistant and AI analyzer each of those button direct you to the page
    with st.sidebar:
        st.title("**Navigation**")
        st.divider()
        st.title("**Quick Access**")
        if st.button(" Home", use_container_width=True, key="nav_home_cy"):
            st.session_state.current_page = "home"; st.rerun()

        st.button(" Cyber Security", use_container_width=True, key="nav_cy_disabled")
        

        if st.button(" Data Science", use_container_width=True, key="nav_data_cy"):
            st.session_state.current_page = "data_science"; st.rerun()

        if st.button(" IT Operations", use_container_width=True, key="nav_ops_cy"):
            st.session_state.current_page = "it_operations"; st.rerun()

        st.divider() #Create a horizontal line to seperate the quick access from the AI
        st.title("**Artificial Intelligence**")
        if st.button(" AI Assistant", use_container_width=True, key="nav_ai_assistant_cy"):
            st.session_state.current_page = "gemini_api_streamlit"; st.rerun()

        if st.button(" AI Analyzer", use_container_width=True, key="nav_ai_analyzer_cy"):
            st.session_state.current_page = "AI_analyzer"; st.rerun()

        st.divider()
        st.title("**Setting**") #Contains the log out buttons
        if st.button("Log Out", use_container_width=True, key="nav_logout_cy"):
            st.session_state.user_logged_in = False
            st.session_state.current_page = "home"; st.rerun()

    # Database section in the dashboard this is where the database is displayed  using pandas so as to output it in a tabular format
    st.header("**Database**")
    try:
        data = get_all_incidents()
        if isinstance(data, pd.DataFrame) and not data.empty:
            st.session_state.cyber_data = data
            st.dataframe(data, height=200)
        else:
            st.info("No data found")
            st.session_state.cyber_data = pd.DataFrame()
    except Exception as error:
        st.error(f"Database error: {error}")
        st.session_state.cyber_data = pd.DataFrame()

    # This is the analytics chart is displayed using the severity and category from the database
    st.divider()
    st.header("**Analytics Charts**")
    df = st.session_state.get("cyber_data", pd.DataFrame())
    if not df.empty:
        #Bar chart is used to displayed the category of the incidents from the database
        colors = ["#b65a5a",'#8b0000','#800000','#deb887','#f28500','#536878']
        col1, col2 = st.columns(2)
        with col1:
            if 'category' in df.columns:
                counts = df['category'].value_counts()
                fig1 = px.bar(x=counts.index, y=counts.values, title="By Category",
                              color=counts.index, color_discrete_sequence=colors)
                st.plotly_chart(fig1, use_container_width=True)
        #Pie chart is used to show the level of severity of the incidents from the database
        with col2:
            if 'severity' in df.columns:
                counts = df['severity'].value_counts()
                fig2 = px.pie(values=counts.values, names=counts.index, title="Severity",
                              hole=0.3, color=counts.index, color_discrete_sequence=colors)
                fig2.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No data for charts")

    # This is where user can add, delete and update incidents
    st.divider()
    st.header("**SQL Crud Operations**")
    tab1, tab2, tab3 = st.tabs([" Add Incident", " Update Incident", " Delete Incident"]) #Tabs allows the crud operations to be displayed after each other

    #Choices is given for adding the incident for category, severity and status
    with tab1:
        category = st.selectbox("Category", ["Malware","Phishing","DDoS","Unauthorised Access","Misconfiguration"], key="cy_add_cat")
        severity = st.selectbox("Severity", ["High","Medium","Low","Critical"], key="cy_add_sev")
        description = st.text_area("Description", key="cy_add_desc")
        status = st.selectbox("Status", ["Open","In Progress","Closed","Resolved"], key="cy_add_stat")
        if st.button(" Add Incident", use_container_width=True, key="cy_btn_add"):

                created_at = str(pd.Timestamp.now()) 
                try:
                    incident_id = insert_incident(created_at, category, severity, status, description)
                    st.success(f"Added incident #{incident_id}") #This displays a successfully added incident message
                    st.rerun()
                except Exception as error:
                    st.error(f"Add failed: {error}") #If incident is failed to add instead of crashing the program try except is used so that this message is displayed 
            
    #Here also choices are displayed to choose from to update the incident status
    with tab2:
        df = st.session_state.get("cyber_data", pd.DataFrame())
        if not df.empty and 'incident_id' in df.columns:
            incident_id = st.selectbox("Select Incident ID", df['incident_id'].tolist(), key="cy_up_id")
            new_status = st.selectbox("New Status", ["Open","Closed","In Progress","Resolved"], key="cy_up_stat")
            if st.button(" Update Incident", use_container_width=True, key="cy_btn_update"):
                try:
                    rows = update_incident_status(incident_id, new_status) #When the button Add Incident is press the update is recorded
                    if rows:
                        st.success(f"Updated incident #{incident_id}")
                        st.rerun()
                    else:
                        st.error("Update failed")
                except Exception as error:
                    st.error(f"Update failed: {error}")
        else:
            st.info("No incidents available to update")

    with tab3:
        df = st.session_state.get("cyber_data", pd.DataFrame())
        if not df.empty and 'incident_id' in df.columns:
            incident_id = st.selectbox("Incident ID to Delete", df['incident_id'].tolist(), key="cy_del_id")
            if st.button(" Delete Incident", use_container_width=True, key="cy_btn_delete"):
                try:
                    rows = delete_incident(incident_id) #Row is deleted when the button Delete Incident is pressed
                    if rows:
                        st.warning(f"Deleted incident #{incident_id}")
                        st.rerun()
                    else:
                        st.error("Delete failed")
                except Exception as error:
                    st.error(f"Delete failed: {error}")
        else:
            st.info("No incidents available to delete")


if __name__ == "__main__":
    cybersecurity_main()
    
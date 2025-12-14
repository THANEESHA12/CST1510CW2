import streamlit as st
from google import genai
from google.genai import types
from app.data.incidents import get_all_incidents
from app.data.datasets import get_all_datasets
from app.data.tickets import get_all_tickets

def ai_analyzer_main():
    st.set_page_config(page_title="AI Analyzer", layout="wide")

    st.session_state.show_register = False
    st.session_state.show_login = False

    with st.sidebar:
        st.title("**Navigation**")
        st.divider()
        st.title("**Quick Access**")
        if st.button("Home", key="nav_home_an"):
            st.session_state.current_page = "home"; st.rerun()
        if st.button("Cyber Security", key="nav_cy_an"):
            st.session_state.current_page = "cybersecurity"; st.rerun()
        if st.button("Data Science", key="nav_ds_an"):
            st.session_state.current_page = "data_science"; st.rerun()
        if st.button("IT Operations", key="nav_ops_an"):
            st.session_state.current_page = "it_operations"; st.rerun()
        if st.button("AI Assistant", key="analyzer_nav_gemini"):
            st.session_state.current_page = "gemini_api_streamlit"; st.rerun()

       

        st.divider()
        st.title("**Artificial Intelligence**")
        if st.button("AI Assistant", use_container_width=True, key="nav_ai_assistant_an"):
            st.switch_page("gemini_api_streamlit.py")
        st.button("AI Analyzer", use_container_width=True, disabled=True, key="nav_ai_analyzer_disabled")

        st.divider()
        st.title("**Setting**")
        if st.button("Logout", use_container_width=True, key="an_logout"):
            st.session_state.user_logged_in = False
            st.session_state.username = None
            st.session_state.user_role = None
            st.success("Logged out.")
            st.switch_page("streamlit_code/home.py")

    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

    # AI analyzer for the cybersecurity domain 
    st.subheader("AI Incident Analyzer")
    incidents_df = get_all_incidents()
    if not incidents_df.empty:
        incident_options = [
            f"{row['incident_id']}: {row['status']} - {row['severity']}"
            for _, row in incidents_df.iterrows()
        ]
        selected_inc_idx = st.selectbox(
            "Select Incident to analyze:",
            range(len(incidents_df)),
            format_func=lambda i: incident_options[i],
            key="an_inc_select",
        )
        incident = incidents_df.iloc[selected_inc_idx]
        st.subheader("Incident Details") #The details on the selected incident will be displayed
        st.write(f"Category: {incident['category']}")
        st.write(f"Severity: {incident['severity']}")
        st.write(f"Description: {incident['description']}")
        st.write(f"Status: {incident['status']}")
        
        #An analysing button is displayed so that user can click on it to analyze their selected incident
        if st.button("Analyze incident with AI", key=f"analyze_incident_{incident['incident_id']}"):
            with st.spinner("AI analyzing incident..."):
                prompt = f"""Analyze this cybersecurity incident:
Category: {incident['category']}
Severity: {incident['severity']}
Description: {incident['description']}
Status: {incident['status']}

Provide:
1. Root cause analysis
2. Immediate actions needed
3. Long-term prevention measures
"""
                response = client.models.generate_content_stream(
                    model="gemini-2.5-flash",
                    config=types.GenerateContentConfig(system_instruction="You are a cybersecurity expert."),
                    contents={"role": "user", "parts": [{"text": prompt}]},
                )
                full = ""
                st.subheader("AI Analysis")
                container = st.empty()
                for chunk in response:
                    full += chunk.text
                    container.markdown(full) #Returning response in full reply

    st.divider()

    #AI analyzer for the data science domain
    st.subheader("AI Dataset Analyzer")
    datasets_df = get_all_datasets()
    if not datasets_df.empty:
        dataset_options = [
            f"{row['dataset_id']}: {row['name']} - {row['rows']} rows"
            for _, row in datasets_df.iterrows()
        ]
        selected_ds_idx = st.selectbox(
            "Select dataset to analyze:",
            range(len(datasets_df)),
            format_func=lambda i: dataset_options[i],
            key="an_ds_select",
        )
        dataset = datasets_df.iloc[selected_ds_idx]
        st.subheader("Dataset Details") #The selected dataset incident will be displayed
        st.write(f"Name: {dataset['name']}")
        st.write(f"Rows: {dataset['rows']}")
        st.write(f"Columns: {dataset['columns']}")
        st.write(f"Uploaded By: {dataset['uploaded_by']}")
        st.write(f"Upload Date: {dataset['upload_date']}")
        
        #The selected dataset can be analyze by using this button
        if st.button("Analyze dataset with AI", key=f"analyze_dataset_{dataset['dataset_id']}"):
            with st.spinner("AI analyzing dataset..."):
                prompt = f"""Analyze this dataset:
Name: {dataset['name']}
Rows: {dataset['rows']}
Columns: {dataset['columns']}
Uploaded By: {dataset['uploaded_by']}
Upload Date: {dataset['upload_date']}

Provide:
- Data quality concerns
- Suggested cleaning steps
- Useful exploratory visuals
- Potential modeling directions
"""
                response = client.models.generate_content_stream(
                    model="gemini-2.5-flash",
                    config=types.GenerateContentConfig(system_instruction="You are a data analyst."),
                    contents={"role": "user", "parts": [{"text": prompt}]},
                )
                full = ""
                st.subheader("AI Analysis")
                container = st.empty()
                for chunk in response:
                    full += chunk.text
                    container.markdown(full) #Returning response in full

    st.divider()

    #This is the IT Operations AI analyzer
    st.subheader("AI IT Tickets Analyzer")
    tickets_df = get_all_tickets()
    if not tickets_df.empty:
        ticket_options = [
            f"{row['ticket_id']}: {row['description'][:30]}... - {row['priority']} ({row['status']})"
            for _, row in tickets_df.iterrows()
        ]
        selected_tk_idx = st.selectbox(
            "Select ticket to analyze:",
            range(len(tickets_df)),
            format_func=lambda i: ticket_options[i],
            key="an_tk_select",
        )
        ticket = tickets_df.iloc[selected_tk_idx]
        st.subheader("Ticket Details") #Displaying the information about the IT Tickets selected
        st.write(f"Ticket ID: {ticket['ticket_id']}")
        st.write(f"Priority: {ticket['priority']}")
        st.write(f"Description: {ticket['description']}")
        st.write(f"Status: {ticket['status']}")
        st.write(f"Assigned To: {ticket['assigned_to']}")
        st.write(f"Created Date: {ticket['created_at']}")
 
        #Selecyes ticket can be analyze by using this button
        if st.button("Analyze ticket with AI", key=f"analyze_ticket_{ticket['ticket_id']}"):
            with st.spinner("AI analyzing ticket..."):
                prompt = f"""Analyze this IT support ticket:
Ticket ID: {ticket['ticket_id']}
Priority: {ticket['priority']}
Description: {ticket['description']}
Status: {ticket['status']}
Assigned To: {ticket['assigned_to']}
Created Date: {ticket['created_at']}

Provide:
- Root cause hypothesis
- Immediate action checklist
- Escalation or closure guidance
- Preventative measures
"""
                response = client.models.generate_content_stream(
                    model="gemini-2.5-flash",
                    config=types.GenerateContentConfig(system_instruction="You are an IT operations expert."),
                    contents={"role": "user", "parts": [{"text": prompt}]},
                )
                full = ""
                st.subheader("AI Analysis")
                container = st.empty()
                for chunk in response:
                    full += chunk.text
                    container.markdown(full.strip()) #Answer is returned using full response

if __name__ == "__main__":
    ai_analyzer_main()

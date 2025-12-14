import streamlit as st
import pandas as pd
import plotly.express as px #Plotly is used to display and build graphs
import os, sys

# Adding path for the database and to be able to import those functions from tickets
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.data.tickets import get_all_tickets, insert_ticket, update_tickets_status, delete_ticket
from app.data.db import connect_database

def itoperations_main():
    st.set_page_config(page_title="IT Operations", layout="wide")
    st.session_state.show_register = False
    st.session_state.show_login = False
    
    #Printing a title for the IT Operation dashboard
    st.title("**IT OPERATIONS DASHBOARD**")
    st.divider()

    # Sidebar navigation that contains different buttons and each gets directed to their pages
    with st.sidebar:
        st.title("**Navigation**")
        st.divider()
        st.title("**Quick Access**")
        if st.button("Home", use_container_width=True, key="nav_home_ops"):
            st.session_state.current_page = "home"
            st.rerun()

        if st.button("Cyber Security", use_container_width=True, key="nav_cy_ops"):
            st.session_state.current_page = "cybersecurity"
            st.rerun()

        if st.button("Data Science", use_container_width=True, key="nav_ds_ops"):
            st.session_state.current_page = "data_science"
            st.rerun()

        st.button("IT Operations", use_container_width=True, disabled=True, key="nav_ops_disabled")

        st.divider()
        st.title("**Artificial Intelligence**")
        if st.button("AI Assistant", use_container_width=True, key="nav_ai_assistant_ops"):
            st.session_state.current_page = "gemini_api_streamlit"
            st.rerun()

        if st.button("AI Analyzer", use_container_width=True, key="nav_ai_analyzer_ops"):
            st.session_state.current_page = "AI_analyzer"
            st.rerun()

        st.divider()
        st.title("**Setting**")
        if st.button("Log Out", use_container_width=True, key="nav_logout_ops"):
            st.session_state.user_logged_in = False
            st.session_state.current_page = "home"
            st.rerun()

    #This is where the database is loaded at in the pd.Dataframe using pandas
    st.header("**Database**")
    try:
        data = get_all_tickets()
        if isinstance(data, pd.DataFrame) and not data.empty:
            st.session_state.ops_data = data
            st.dataframe(data, height=200)
        else:
            st.info("No data found")
            st.session_state.ops_data = pd.DataFrame()
    except Exception as error:
        st.error(f"Database error: {error}")
        st.session_state.ops_data = pd.DataFrame()

    #This is the analytic chart of the domain
    st.divider()
    st.header("**Analytics Charts**")
    df = st.session_state.get("ops_data", pd.DataFrame())
    if not df.empty:
        colors = ['#f08080','#8b0000','#800000','#deb887','#f28500','#536878']
        #The charts are displayed side by side
        col1, col2 = st.columns(2)
        with col1:
            #This is creating a bar chart based on the priority of the tickets
            if 'priority' in df.columns:
                counts = df['priority'].value_counts()
                fig1 = px.bar(x=counts.index, y=counts.values, title="By Priority",
                              color=counts.index, color_discrete_sequence=colors)
                st.plotly_chart(fig1, use_container_width=True)
        with col2:
            #A pie chart is created based on the status of the tickets
            if 'status' in df.columns:
                counts = df['status'].value_counts()
                fig2 = px.pie(values=counts.values, names=counts.index, title="Status",
                              hole=0.3, color=counts.index, color_discrete_sequence=colors)
                fig2.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No data for charts")

    #Performing the crud operations
    st.divider()
    st.header("**SQL Crud Operations**")
    tab1, tab2, tab3 = st.tabs(["Add Tickets", "Update Tickets", "Delete Tickets"])

    #Adding tickets to the database and for different section different option is given to choose from or to type in
    with tab1:
        priority = st.selectbox("Priority", ["High","Medium","Low","Critical"], key="ops_add_priority")
        status = st.selectbox("Status", ["Open","In Progress","Resolved","Waiting for user"], key="ops_add_status")
        description = st.text_area("Description", key="ops_add_desc")
        assigned_to = st.text_input("Assigned To (optional)", key="ops_add_assigned")
        resolution_time_hours = st.number_input("Resolution Time (hours, optional)", min_value=0.0, value=0.0, step=0.5, key="ops_add_res_hours")
        time_hours = st.number_input("Worked Time (hours, optional)", min_value=0.0, value=0.0, step=0.5, key="ops_add_time_hours")

        if st.button("Add Ticket", use_container_width=True, key="ops_btn_add"):
            if description.strip():
                try:
                    ticket_id = insert_ticket(
                        priority=priority,
                        status=status,
                        description=description.strip(),
                        assigned_to=assigned_to if assigned_to else None,
                        resolution_time_hours=resolution_time_hours if resolution_time_hours > 0 else None,
                        time_hours=time_hours if time_hours > 0 else None
                    )
                    st.success(f"Added ticket #{ticket_id}")
                    st.rerun()
                except Exception as error:
                    st.error(f"Add failed: {error}")
            else:
                st.error("Enter a description")

    #Updating tickets from the database table
    with tab2:
        df = st.session_state.get("ops_data", pd.DataFrame())
        if not df.empty and 'ticket_id' in df.columns:
            ticket_id = st.selectbox("Select Ticket ID", df['ticket_id'].tolist(), key="ops_update_id")
            new_status = st.selectbox("New Status", ["Open","In Progress","Resolved","Waiting for user"], key="ops_update_status")
            if st.button("Update Ticket", use_container_width=True, key="ops_btn_update"):
                try:
                    conn = connect_database() #Creating a connection to the database
                    rows_updated = update_tickets_status(conn, ticket_id, new_status) #This will update the row on the database
                    conn.close() #Closing a connection to the database
                    if rows_updated:
                        st.success(f"Updated ticket #{ticket_id} → {new_status}") #A success message will be displayed
                        st.rerun()
                    else:
                        st.error("Update failed")
                except Exception as error:
                    st.error(f"Update failed: {error}")
        else:
            st.info("No tickets available to update")

    #Deleting process from the databse table
    with tab3:
        df = st.session_state.get("ops_data", pd.DataFrame())
        if not df.empty and 'ticket_id' in df.columns:
            ticket_id = st.selectbox("Ticket ID to Delete", df['ticket_id'].tolist(), key="ops_delete_id")
            if st.button("Delete Ticket", use_container_width=True, key="ops_btn_delete"):
                try:
                    conn = connect_database() #Creating a connection to the database
                    rows_deleted = delete_ticket(conn, ticket_id) #The row is deleted thus this is recorded here
                    conn.close() #Closing a connection to the database
                    if rows_deleted:
                        st.warning(f"Deleted ticket #{ticket_id}")
                        st.rerun()
                    else:
                        st.error("Delete failed")
                except Exception as error:
                    st.error(f"Delete failed: {error}")
        else:
            st.info("No tickets available to delete")

if __name__ == "__main__":
    itoperations_main()

import streamlit as st
import pandas as pd
import plotly.express as px
import os, sys

#Adding path for database and to be able to import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.data.datasets import get_all_datasets, insert_dataset, update_dataset, delete_dataset

def data_science_main():
    st.set_page_config(page_title="Data Science", layout="wide")
    st.session_state.show_register = False
    st.session_state.show_login = False

    st.title("**DATA SCIENCE DASHBOARD**") #Displays a title for the data science dashboard
    st.divider()

    #Creating a navigation bar that contains different feature and each of them is enter their pages
    with st.sidebar:
        st.title("**Navigation**")
        st.divider()
        st.title("**Quick Access**")
        if st.button("Home", use_container_width=True, key="nav_home_ds"):
            st.session_state.current_page = "home"
            st.rerun()

        if st.button("Cyber Security", use_container_width=True, key="nav_cy_ds"):
            st.session_state.current_page = "cybersecurity"
            st.rerun()

        st.button("Data Science", use_container_width=True, disabled=True, key="nav_ds_disabled")

        if st.button("IT Operations", use_container_width=True, key="nav_ops_ds"):
            st.session_state.current_page = "it_operations"
            st.rerun()

        st.divider()
        st.title("**Artificial Intelligence**")
        if st.button("AI Assistant", use_container_width=True, key="nav_ai_assistant_ds"):
            st.session_state.current_page = "gemini_api_streamlit"
            st.rerun()

        if st.button("AI Analyzer", use_container_width=True, key="nav_ai_analyzer_ds"):
            st.session_state.current_page = "AI_analyzer"
            st.rerun()

        st.divider()
        st.title("**Setting**")
        if st.button("Log Out", use_container_width=True, key="nav_logout_ds"):
            st.session_state.user_logged_in = False
            st.session_state.current_page = "home"
            st.rerun()

    #This is where the database is displayed on the data science dashboard using pandas
    #Pandas makes this cleaner and easy to ready through as it is more organised
    st.header("**Database**")
    try:
        data = get_all_datasets()
        if isinstance(data, pd.DataFrame) and not data.empty:
            st.session_state.ds_data = data
            st.dataframe(data, height=200)
        else:
            st.info("No data found")
            st.session_state.ds_data = pd.DataFrame()
    except Exception as error:
        st.error(f"Database error: {error}")
        st.session_state.ds_data = pd.DataFrame()

    #Displaying charts based the uploaded_by and rows
    st.divider()
    st.header("**Analytics Charts**")
    df = st.session_state.get("ds_data", pd.DataFrame())
    if not df.empty:
        colors = ['#f08080','#8b0000','#800000','#deb887','#f28500','#536878']
        col1, col2 = st.columns(2)
        with col1:
            #A bar chart is created to display the followings
            if 'uploaded_by' in df.columns:
                counts = df['uploaded_by'].value_counts()
                fig1 = px.bar(x=counts.index, y=counts.values, title="By Uploader",
                              color=counts.index, color_discrete_sequence=colors)
                st.plotly_chart(fig1, use_container_width=True)
        with col2:
            if 'rows' in df.columns:
                data_copy = df.copy()
                data_copy['size'] = pd.cut(data_copy['rows'],
                                           bins=[0,1000,5000,10000,float('inf')],
                                           labels=['Small','Medium','Large','Huge'])
                sizes = data_copy['size'].value_counts()
                fig2 = px.pie(values=sizes.values, names=sizes.index, title="Size Distribution",
                              hole=0.3, color=sizes.index, color_discrete_sequence=colors)
                st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No data for charts")

    #Crud operations to be able to add, delete and update datasets.
    st.divider()
    st.header("**SQL Crud Operations**")
    tab1, tab2, tab3 = st.tabs(["Add Dataset", "Update Dataset", "Delete Dataset"])

    # This is where the dataset is added if the add dataset is pressed and it does straight on the database
    with tab1:
        name = st.text_input("Dataset Name", key="ds_add_name")
        rows = st.number_input("Rows", min_value=1, value=100, key="ds_add_rows")
        columns = st.number_input("Columns", min_value=1, value=5, key="ds_add_cols")
        uploader = st.selectbox("Uploaded By", ["data_scientist","it_admin","cyber_admin"], key="ds_add_uploader")

        if st.button("Add Dataset", use_container_width=True, key="ds_btn_add"):
            if name.strip():
                try:
                    dataset_id = insert_dataset(
                        name.strip(),
                        int(rows),
                        int(columns),
                        uploader,
                        pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                    )
                    st.success(f"Added dataset #{dataset_id}")
                    st.rerun()
                except Exception as error:
                    st.error(f"Add failed: {error}")
            else:
                st.error("Enter a name")

    #Updating the dataset by selecting and entering the updates
    with tab2:
        df = st.session_state.get("ds_data", pd.DataFrame())
        if not df.empty and 'dataset_id' in df.columns:
            dataset_id = st.selectbox("Select Dataset ID", df['dataset_id'].tolist(), key="ds_update_id")
            new_rows = st.number_input("New Rows", min_value=1, value=100, key="ds_update_rows")
            new_columns = st.number_input("New Columns", min_value=1, value=5, key="ds_update_cols")
            new_name = st.text_input("New Name", key="ds_update_name")

            if st.button("Update Dataset", use_container_width=True, key="ds_btn_update"):
                try:
                    rows_updated = update_dataset(dataset_id, int(new_rows), int(new_columns), new_name.strip()) #After using filling the form and pressing add incident the row is updated as information is being added
                    if rows_updated:
                        st.success(f"Updated dataset #{dataset_id}")
                        st.rerun()
                    else:
                        st.error("Update failed")
                except Exception as error:
                    st.error(f"Update failed: {error}")
        else:
            st.info("No datasets available to update")

    #This is where dataset can be deleted from the table
    with tab3:
        df = st.session_state.get("ds_data", pd.DataFrame())
        if not df.empty and 'dataset_id' in df.columns:
            dataset_id = st.selectbox("Dataset ID to Delete", df['dataset_id'].tolist(), key="ds_delete_id")
            if st.button("Delete Dataset", use_container_width=True, key="ds_btn_delete"):
                try:
                    rows_deleted = delete_dataset(dataset_id) #This is where the row is deleted
                    if rows_deleted:
                        st.warning(f"Deleted dataset #{dataset_id}")
                        st.rerun()
                    else:
                        st.error("Delete failed")
                except Exception as error:
                    st.error(f"Delete failed: {error}")
        else:
            st.info("No datasets available to delete")

if __name__ == "__main__":
    data_science_main()

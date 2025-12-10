# Pandas is imported do that the databse can be displayed in a form of table
import pandas as pd
from app.data.db import connect_database #from db the function connect_database is being imported

#This function is checking whether my datasets_metadata table exists
def table_exists_check():
    """Check if datasets_metadata table exists"""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='datasets_metadata'
    """)
    exists = cursor.fetchone() is not None
    conn.close()
    return exists


#This function is inserting datasets details 
def insert_dataset(name, rows, columns, uploaded_by, upload_date):
    """Insert new dataset - SAME PATTERN AS insert_incident"""
    conn = connect_database() #Opening a connection to the database
    cursor = conn.cursor() #A cursor is created to run the SQL commands
    
    # Create file path
    file_path = f"/data/{name.lower().replace(' ', '_')}.csv" #Building a file path
    
    #Running the SQL command INSERT to add new row into the datasets_metadata
    #Placeholders is being used to insert values properly without causing injections
    cursor.execute("""
        INSERT INTO datasets_metadata
        (name, file_path, rows, columns, uploaded_by, upload_date)
        VALUES (?, ?, ?, ?, ?, ?) 
    """, (name, file_path, rows, str(columns), uploaded_by, upload_date)) #Storing all the details
    
    conn.commit() #Saving the changes in the database
    dataset_id = cursor.lastrowid #Fetches the auto-generated ID of the new dataset row inserted
    conn.close() #Closing the database connection 
    
    return dataset_id #Returning the dataset_id uniquely of the inserted row

#This function fetches all the dataset records from the table
def get_all_datasets():
    """Get all datasets - SAME PATTERN AS get_all_incidents"""
    #This checks if the table exists by calling a function
    if not table_exists_check():
        print("Table datasets_metadata does not exist") ##if table does not exists it prints a message instead of crashing it
        return pd.DataFrame() 
    
    conn = connect_database() #Opening a connection to the database
    #Using SQL with pandas to run
    df = pd.read_sql_query(
        "SELECT * FROM datasets_metadata ORDER BY dataset_id DESC",
        conn
    )
    conn.close()
    return df

#Defining a function to update the dataset by passing parameters
def update_dataset(dataset_id, new_rows=None, new_columns=None, new_name=None):
    """Update dataset - SAME PATTERN AS update_incident_status"""
    conn = connect_database() #Opening a connection to the database
    cursor = conn.cursor() #A cursor is created to run the SQL commands
    
    #These empty list collects the values and updates
    updates = []
    values = []
    
    #Checking which field is to be updated
    if new_rows is not None:
        updates.append("rows = ?")
        values.append(new_rows)
    if new_columns is not None:
        updates.append("columns = ?")
        values.append(str(new_columns))
    if new_name is not None:
        updates.append("name = ?")
        values.append(new_name)
    
    #If there are any updated it will then join the SQL commands for update
    if updates:
        values.append(dataset_id)
        update_query = f"""
            UPDATE datasets_metadata 
            SET {', '.join(updates)} 
            WHERE dataset_id = ?
        """
        cursor.execute(update_query, values) #The query is executed with the values
        conn.commit() #Saving the changes in the database
        rows_updated = cursor.rowcount #This will let you know how many rows were actually updated
    else:
        rows_updated = 0 #This will be returned if there is no update
    
    conn.close()
    return rows_updated

#This function is defined to remove dataset record from the table and takes dataset_id as parameter which will be used for the deletion
def delete_dataset(dataset_id):
    """Delete a dataset - SAME PATTERN AS delete_incident"""
    conn = connect_database() #Opening a connection to the databse
    cursor = conn.cursor() #A cursor is created to run the SQL commands
    
    #The cursor is running an SQL command DELETE which will remove the row from the table where the dataset_id matches
    cursor.execute("""
        DELETE FROM datasets_metadata WHERE dataset_id = ?
    """, (dataset_id,)) #(dataset_id) helps avoiding injections
    
    conn.commit() #Saving the deleted process
    rows_deleted = cursor.rowcount #Checking how many rows were deleted
    conn.close() #Closing the connection to the databse
    
    return rows_deleted #Returning the number of rows delete this shows you if deletion was completed ot not


# Testing if the function works
if __name__ == "__main__":
    conn = connect_database()
    
    print("\n Testing Dataset Functions:")
    print("-" * 30)
    
    # Test get_all_datasets
    datasets = get_all_datasets()
    print(f"Found {len(datasets)} datasets")
    
    if not datasets.empty:
        print("\nFirst few datasets:")
        print(datasets[['dataset_id', 'name', 'rows', 'uploaded_by']].head())
    
    conn.close()
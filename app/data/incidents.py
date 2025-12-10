import pandas as pd #Pandas is used to create tables
from app.data.db import connect_database #from db the function connect_database is being imported

#This function checks if the cyber_incidents table exists or not
def table_exists_check():
    #checking if the cyber_incidents table exists
    conn = connect_database() #Opening a connection to the database
    cursor = conn.cursor() #A cursor is created to run SQL commands
    #sqlite_master keeps track of the table thus here it is looking for cyber_incidents 
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='cyber_incidents'
    """)
    exists = cursor.fetchone() is not None #Returning the first row if the table exists or None if it does not exists
    conn.close() #Closing the connection to the database
    return exists #If table is found exists will be True if not exists will be False


#This function is defined to add new incident into the table that is cyber_incidents and save the details that is being passed as the parameters
def insert_incident(timestamp, category, severity, status, description):
    """Insert new incident."""
    conn = connect_database() #Opening a connection to the database
    cursor = conn.cursor() #A cursor is created to run the SQL commands which in this case is INSERT INTO
    #The cursor execute to run the SQL command INSERT to add a new row into the table and '?' placeholder fills the information and keeps query to avoid SQL injection
    cursor.execute("""
        INSERT INTO cyber_incidents
        (timestamp, category, severity, status, description)
        VALUES (?, ?, ?, ?, ?)
    """, (timestamp, category, severity, status, description))
    conn.commit() #Saving the new record in the database
    incident_id = cursor.lastrowid #Fetched an ID for the recent inserted incident
    conn.close() #Closing the connection to the database
    return incident_id #Returning the id of the recent incident insert

#This function is defined to fetch records from the table
def get_all_incidents():
    """Get all incidents as DataFrame."""
    #Checking if the table exists and if it does not exists a message is displayed thus preventing the program to crash
    if not table_exists_check():
        print("Table cyber_incidents does not exists")
        return pd.DataFrame()
    
    conn = connect_database() #Opening a connection to the database
    #Using pandas to run the SQL query in which it fetched the row and columns from the table 
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents ORDER BY incident_id DESC",
        conn
    )
    conn.close() #Closing connection to the databse
    return df #Returning the df with all the incidences

#This function is being defined to update the incident status by using incident_id that updates the incident_id and new_status that is Open, Resolved and Closed
def update_incident_status(incident_id, new_status):
    """Update status of an incident."""
    conn = connect_database() #Opening a connection to the database
    cursor = conn.cursor() #A cursor is created to run SQL commands which in this case is UPDATE
    #The cursor is being executed and is setting the status where the incident_id matches
    cursor.execute("""
        UPDATE cyber_incidents SET status = ? WHERE incident_id = ?""", (new_status, incident_id)
        )
    conn.commit() #This is saving the changes the update in the database
    rows_updated = cursor.rowcount #Indicated how many rows were updated
    conn.close() #Closing the connection to the database
    return rows_updated 

#This function is being defined to remove incidents from the table and takes incident_id for the deletion process
def delete_incident(incident_id):
    """
    Delete an incident from the database.
    """
    conn = connect_database() #Opening a connection to the databse
    cursor = conn.cursor() #A cursor is created to run the SQL command
    #The cursor is executing the DELETE command in which rows are removed where the incident_id matches the one being passed
    cursor.execute("""
        DELETE FROM cyber_incidents WHERE incident_id = ?""", (incident_id,)
        )
    conn.commit() #Saving the deletion in the databse
    rows_deleted = cursor.rowcount #Checking how many rows were deleted
    conn.close() #Closing the connection to the databse
    return rows_deleted

#This function is being defined to count incidences in each category
def get_incidents_by_type_count():
    """
    Count incidents by type.
    Uses: SELECT, FROM, GROUP BY, ORDER BY
    """
    conn = connect_database() #Opening a connection to the databse
    #Performing an SQL query in which SELECT fetched each category and counts how many rows belong to that category , FROM looks to the table, GROUP BY will ground the incidents by their category and ORDER BY sorts the results which will therefore show the incidents that happens the most
    query = """
    SELECT category, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY category
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn) #pd will make it more easier to read
    conn.close() #Closing the connection to the database
    return df

#This function is being defined that get the high-severity incidents that exists by status that is Open, Resolved or Closed
def get_high_severity_by_status():
    """
    Count high severity incidents by status.
    Uses: SELECT, FROM, WHERE, GROUP BY, ORDER BY
    """
    conn = connect_database() #Opening a connection to the database
    #SELECT will fetch the status and counts the rows belonging to it , FROM will look at the table, WHERE will get the incidents that have high severity, GROUP BY will filter the incidents by their status and ORDER BY will sort the result with the high severity
    query = """
    SELECT status, COUNT(*) as count
    FROM cyber_incidents
    WHERE severity = 'High'
    GROUP BY status
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn) #Makes it easier to read later when using pd
    conn.close() #Closing the connection to the database
    return df

#This function is being defined to get incident types with many cases 
def get_incident_types_with_many_cases(min_count=5):
    """
    Find incident types with more than min_count cases.
    Uses: SELECT, FROM, GROUP BY, HAVING, ORDER BY
    """
    conn = connect_database() #Opening a connection to the database
    #The SELECT eill fetch each categories and count the rows for that incident, FROM the table, GROUP BY which will group them by their category for eg phishing, HAVING COUNT will filter out categories with fewer cases and ORDER BY will sprts the category with the most incidents
    query = """
    SELECT category, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY category
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn, params=(min_count,)) #params safely passess the min_count values into the query
    conn.close() #Closing the database connection
    return df

# Test: Run analytical queries
if __name__ == "__main__":
    conn = connect_database()

    print("\n All Incidents:")
    print(get_all_incidents())

    print("\n Incidents by Type:")
    df_by_type = get_incidents_by_type_count()
    print(df_by_type)

    print("\n High Severity Incidents by Status:")
    df_high_severity = get_high_severity_by_status()
    print(df_high_severity)

    print("\n Incident Types with Many Cases (>5):")
    df_many_cases = get_incident_types_with_many_cases(min_count=5)
    print(df_many_cases)

    conn.close()


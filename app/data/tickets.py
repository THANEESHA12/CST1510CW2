import pandas as pd #Pandas is being imported for the creation of table
from app.data.db import connect_database

#This function is being defined to be able to add new tickets in the table
def insert_ticket(priority, status, description, assigned_to = None, resolution_time_hours =  None, time_hours = None):
    """Insert new It tickets"""
    conn = connect_database() #Opening a connection to the database
    cursor = conn.cursor() #A cursor is created to run the SQL commands
    #The cursor is being executed and '?' placeholders to avoid SQL injections
    cursor.execute("""
        INSERT INTO it_tickets
        (priority, status, description, assigned_to, resolution_time_hours, time_hours)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (priority, status, description, assigned_to, resolution_time_hours, time_hours))
    conn.commit() #The new tickets details is being saved in the database
    ticket_id = cursor.lastrowid #Fetches unique ID for the inserted row
    conn.close() #Closing the database connection
    return ticket_id

#This function is being defined to get the tickets records from the table
def get_all_tickets():
    """Get all IT tickets as DataFrame."""
    conn = connect_database() #Opening a connection to the database
    #Executing the SQL and loading them in the df
    df = pd.read_sql_query(
        "SELECT ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours, time_hours FROM it_tickets ORDER BY ticket_id DESC",
        conn
    )
    conn.close() #Closing the connection to the database
    return df

#This function is defined to update the ticket status
def update_tickets_status(conn, ticket_id, new_status):
    """
    Update the status of a ticket.

    """
    cursor = conn.cursor() #A cursor is created to run the SQL commands
    #The cursor execute the SQL command 
    cursor.execute("""
        UPDATE it_tickets SET status = ? WHERE ticket_id = ?""", (new_status, ticket_id)
        )
    conn.commit() #The updated details is being saved to the database
    return cursor.rowcount #This provides the number of updated row

#This function is defined to remove ticket_id from the table
def delete_ticket(conn, ticket_id):
    """
    Delete a ticket.
    """
    cursor = conn.cursor() #A cursor is created to run SQL commands
    #The cursor executes the SQL command
    cursor.execute("""
        DELETE FROM it_tickets WHERE ticket_id = ?""", (ticket_id,)
        )
    conn.commit() #The deletion is changed which is then saved in the database
    return cursor.rowcount #The number of rows deleted


    
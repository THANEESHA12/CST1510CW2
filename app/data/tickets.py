import pandas as pd
from app.data.db import connect_database


def insert_ticket(priority, status, category, subject, description, created_date, resolved_date = None, assigned_to = None):
    """Insert new It tickets"""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO it_tickets
        (priority, status, category, subject, description, created_date, resolved_date, assigned_to)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (priority, status, category, subject, description, created_date, resolved_date, assigned_to))
    conn.commit()
    ticket_id = cursor.lastrowid
    conn.close()
    return ticket_id

def get_all_tickets():
    """Get all IT tickets as DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM it_tickets ORDER BY ticket_id DESC",
        conn
    )
    conn.close()
    return df

def update_tickets_status(conn, ticket_id, new_status):
    """
    Update the status of a ticket.

    """
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE it_tickets SET status = ? WHERE ticket_id = ?""", (new_status, ticket_id)
        )
    conn.commit()
    return cursor.rowcount

def delete_ticket(conn, ticket_id):
    """
    Delete a ticket.
    """
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM it_tickets WHERE ticket_id = ?""", (ticket_id,)
        )
    conn.commit()
    return cursor.rowcount


    
import pandas as pd
from app.data.db import connect_database

def table_exists_check():
    #checking if the cyber_incidents table exists
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='cyber_incidents'
    """)
    exists = cursor.fetchone() is not None
    conn.close()
    return exists


def insert_incident(timestamp, category, severity, status, description):
    """Insert new incident."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cyber_incidents
        (timestamp, category, severity, status, description)
        VALUES (?, ?, ?, ?, ?)
    """, (timestamp, category, severity, status, description))
    conn.commit()
    incident_id = cursor.lastrowid
    conn.close()
    return incident_id

def get_all_incidents():
    """Get all incidents as DataFrame."""
    if not table_exists_check():
        print("Table cyber_incidents does not exists")
        return pd.DataFrame()
    
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents ORDER BY incident_id DESC",
        conn
    )
    conn.close()
    return df

def update_incident_status(incident_id, new_status):
    """Update status of an incident."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE cyber_incidents SET status = ? WHERE incident_id = ?""", (new_status, incident_id)
        )
    conn.commit()
    rows_updated = cursor.rowcount
    conn.close()
    return rows_updated

def delete_incident(incident_id):
    """
    Delete an incident from the database.
    """
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM cyber_incidents WHERE incident_id = ?""", (incident_id,)
        )
    conn.commit()
    rows_deleted = cursor.rowcount
    conn.close()
    return rows_deleted

def get_incidents_by_type_count():
    """
    Count incidents by type.
    Uses: SELECT, FROM, GROUP BY, ORDER BY
    """
    conn = connect_database()
    query = """
    SELECT category, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY category
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_high_severity_by_status():
    """
    Count high severity incidents by status.
    Uses: SELECT, FROM, WHERE, GROUP BY, ORDER BY
    """
    conn = connect_database()
    query = """
    SELECT status, COUNT(*) as count
    FROM cyber_incidents
    WHERE severity = 'High'
    GROUP BY status
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_incident_types_with_many_cases(min_count=5):
    """
    Find incident types with more than min_count cases.
    Uses: SELECT, FROM, GROUP BY, HAVING, ORDER BY
    """
    conn = connect_database()
    query = """
    SELECT category, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY category
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn, params=(min_count,))
    conn.close()
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


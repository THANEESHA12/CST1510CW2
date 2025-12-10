# app/data/datasets.py - SAME PATTERN AS CYBER
import pandas as pd
from app.data.db import connect_database

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


def insert_dataset(name, rows, columns, uploaded_by, upload_date):
    """Insert new dataset - SAME PATTERN AS insert_incident"""
    conn = connect_database()
    cursor = conn.cursor()
    
    # Create file path
    file_path = f"/data/{name.lower().replace(' ', '_')}.csv"
    
    cursor.execute("""
        INSERT INTO datasets_metadata
        (name, file_path, rows, columns, uploaded_by, upload_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, file_path, rows, str(columns), uploaded_by, upload_date))
    
    conn.commit()
    dataset_id = cursor.lastrowid
    conn.close()
    
    return dataset_id


def get_all_datasets():
    """Get all datasets - SAME PATTERN AS get_all_incidents"""
    if not table_exists_check():
        print("Table datasets_metadata does not exist")
        return pd.DataFrame()
    
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM datasets_metadata ORDER BY dataset_id DESC",
        conn
    )
    conn.close()
    return df


def update_dataset(dataset_id, new_rows=None, new_columns=None, new_name=None):
    """Update dataset - SAME PATTERN AS update_incident_status"""
    conn = connect_database()
    cursor = conn.cursor()
    
    # Build the update query dynamically
    updates = []
    values = []
    
    if new_rows is not None:
        updates.append("rows = ?")
        values.append(new_rows)
    if new_columns is not None:
        updates.append("columns = ?")
        values.append(str(new_columns))
    if new_name is not None:
        updates.append("name = ?")
        values.append(new_name)
    
    if updates:
        values.append(dataset_id)
        update_query = f"""
            UPDATE datasets_metadata 
            SET {', '.join(updates)} 
            WHERE dataset_id = ?
        """
        cursor.execute(update_query, values)
        conn.commit()
        rows_updated = cursor.rowcount
    else:
        rows_updated = 0
    
    conn.close()
    return rows_updated


def delete_dataset(dataset_id):
    """Delete a dataset - SAME PATTERN AS delete_incident"""
    conn = connect_database()
    cursor = conn.cursor()
    
    cursor.execute("""
        DELETE FROM datasets_metadata WHERE dataset_id = ?
    """, (dataset_id,))
    
    conn.commit()
    rows_deleted = cursor.rowcount
    conn.close()
    
    return rows_deleted


# Optional: Test function (like your cyber code has)
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
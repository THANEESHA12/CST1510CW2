import pandas as pd
import os
from pathlib import Path
from app.data.db import connect_database
import sys

# FIX: Add parent directory to Python path so 'app' can be found
current_folder = Path(__file__).parent  # app/data
app_folder = current_folder.parent  # app
project_root = app_folder.parent  # CST1510CM2

# Add project root to Python path
sys.path.insert(0, str(project_root))
print(f"Working in: {project_root}")

# NOW import
from app.data.db import connect_database

def create_users_table(conn):
    """Create users table."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    """)
    conn.commit()
    print("Users table created successfully!")

    
def create_cyber_incidents_table(conn):
    #Connecting a cursor to create connection
    cursor = conn.cursor() #Getting a cursor from the connection
    #Creating the cyber incidents table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            incident_id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            severity TEXT,
            category TEXT,
            status TEXT,
            description TEXT, 
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP           
        )
    """)
    conn.commit()
    print("Cyber_incident table has been created successfully!")



def create_datasets_metadata_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS datasets_metadata(
                   dataset_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   file_path TEXT NOT NULL,
                   rows INTEGER,
                   columns TEXT,
                   uploaded_by TEXT,
                   upload_date TEXT,
                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    print("Datasets_metadata table has been successfully created!")


def create_it_tickets_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS it_tickets (
                   ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   priority TEXT,
                   description TEXT,
                   status TEXT,
                   assigned_to TEXT,
                   created_at TEXT,
                   resolution_time_hours INTEGER,
                   time_hours INTEGER           
        )
    """)
    conn.commit()
    print("IT tickets table has been successfully created!")


def create_all_tables(conn):
    """Create all tables."""
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)
    print("Tables created successfully")

def load_csv_file(conn, csv_path, table_name):
    """Load one CSV file into a database table"""
    if not os.path.exists(csv_path):
        print(f"❌ File not found: {csv_path}")
        return 0
    
    try:
        # Read the CSV file
        if csv_path.suffix == ".txt":
            df = pd.read_csv(csv_path, sep="\t")  # Tab-separated files
        else:
            df = pd.read_csv(csv_path)  # Comma-separated files
        
        print(f"📖 Reading {csv_path.name}...")

        # SPECIAL HANDLING for datasets_metadata table
        if table_name == "datasets_metadata" and "columns" in df.columns:
            # Convert 'columns' from int to string to match TEXT column type
            df["columns"] = df["columns"].astype(str)
            print(f"   Converted 'columns' to string type")
        
        # Insert into database
        df.to_sql(name=table_name, con=conn, if_exists='append', index=False)
        print(f"✅ Loaded {len(df)} rows into '{table_name}' table")
        return len(df)
    except Exception as e:
        print(f"Error loading {csv_path.name}: {e}")
        return 0
    
def load_all_csv_files(conn):
    """Load all CSV files from the DATA folder"""
    print("\n📁 Looking for CSV files...")
    
    # Go up from app/data to project root, then into DATA folder
    data_folder = Path(__file__).parent.parent.parent.parent / "DATA"
    print(f"📂 Data folder: {data_folder}")
    
    # List of files to load
    files_to_load = {
        "users.txt": "users",
        "cyber_incidents.csv": "cyber_incidents",
        "datasets_metadata.csv": "datasets_metadata",
        "it_tickets.csv": "it_tickets"
    }
    
    total_rows = 0
    
    for filename, table_name in files_to_load.items():
        file_path = data_folder / filename

        if file_path.exists():
            rows_loaded = load_csv_file(conn, file_path, table_name)
            total_rows += rows_loaded
        else:
            print(f"⚠️  Skipping {filename} - not found")
    
    print(f"\n📊 Total rows loaded: {total_rows}")
    return total_rows


def load_all_csv_data(conn, csv_path, table_name):
    if not os.path.exists(csv_path):
        print(f"CSV {csv_path} does not exist.")
        return 0
    
    try:
        # Detect separator
        if csv_path.suffix == ".txt":
            df = pd.read_csv(csv_path, sep="\t")
        else:
            df = pd.read_csv(csv_path)
        
        print(f"Loaded {len(df)} rows from {csv_path.name}")

        df.to_sql(name=table_name, con=conn, if_exists = 'append', index = False)
        print(f"Data successfully inserted in '{table_name}'")
        return len(df)
    except Exception as e:
        print(f"Error occured in loading CSV to table '{table_name}' : {e}")
        return 0

def load_all_csvs(conn):
    """Load all CSVs from DATA folder into their tables."""
    data_folder = Path(__file__).parent.parent.parent.parent / "DATA"
    print(f"CSV files in: {data_folder}")
    files = {
        "users.txt": "users",
        "cyber_incidents.csv": "cyber_incidents",
        "datasets_metadata.csv": "datasets_metadata",
        "it_tickets.csv": "it_tickets"
    }

    total_rows = 0
    for filename, table_name in files.items():
        csv_path = data_folder / filename
        if csv_path.exists():
            rows = load_all_csv_data(conn, csv_path, table_name)
            total_rows += rows
            print(f"Loaded {rows} rows into '{table_name}'")
        else:
            print(f"File not found: {csv_path}")

    print(f"All csv's successfully loaded'")
    return total_rows

if __name__ == "__main__":
    print("\n🚀 STARTING DATABASE SETUP")
    print("-" * 30)
    
    # Step 1: Connect to database
    print("🔗 Connecting to database...")
    conn = connect_database()
    
    # Step 2: Create tables
    create_all_tables(conn)
    
    # Step 3: Load CSV data
    print("\n📥 Loading data from CSV files...")
    rows_loaded = load_all_csv_files(conn)
    
    # Step 4: Show results
    print("\n" + "=" * 50)
    print("📋 DATABASE SUMMARY")
    print("-" * 30)

    cursor = conn.cursor()
    
    # Show all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("\n📊 Tables in your database:")
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"   • {table_name}: {count} rows")
    
    # Close connection
    conn.close()
    
    print("\n" + "=" * 50)
    print("🎉 DATABASE SETUP COMPLETE!")
    print("👉 Now run: streamlit run datascience_domain.py")
    print("=" * 50)
    
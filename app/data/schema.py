import pandas as pd #Importing pandas to be able to create table to read the csv's
import os #This helps in the checking whether a file exists or not
from pathlib import Path 
from app.data.db import connect_database
import sys #Modifying system path by using this module

#Adding parent directory to Python path so 'app' can be found then the import can be used
current_folder = Path(__file__).parent  # current folder is app/data
app_folder = current_folder.parent  #The app folder hold the current_folder.parent
project_root = app_folder.parent  # The root of the folder is found which is CST1510CW2

# Adding project root to Python path
sys.path.insert(0, str(project_root))
print(f"Working in: {project_root}") #A message in which directory is the root

# The connect_database is re-imported which will ensures that the import rowks
from app.data.db import connect_database

#This functions is being defined to created users table by using the db connection
def create_users_table(conn):
    """Create users table."""
    cursor = conn.cursor() #A cursor is created to run the SQL commands
    #The cursor is being executed in which if a user tables does not exists will get created
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    """)
    conn.commit() #The table creation is being saved in the database
    print("Users table created successfully!")


#This function is being defined to create the cyber_incidents table    
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
    conn.commit() #The details is saved to the database
    print("Cyber_incident table has been created successfully!") #This message is displayed if the table was successfully created


#This function is defined to create the datasets_metadata table
def create_datasets_metadata_table(conn):
    cursor = conn.cursor() #Getting a connection from the cursor
    #The cursor is being executed
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
    conn.commit() #The details is being saved in the table
    print("Datasets_metadata table has been successfully created!") #This message is displayed if the table was successfully created


#This function is being defined to create the it_tickets table
def create_it_tickets_table(conn):
    cursor = conn.cursor() #Getting a connection from the cursor
    #The cursor is being executed
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
    conn.commit() #The details is being saved in the table
    print("IT tickets table has been successfully created!") #This message is displayed if the table was successfully created

#This function is being defiend so that all the table gets created
def create_all_tables(conn):
    """Create all tables."""
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)
    print("Tables created successfully") #This message sends a confirmation that all the table was successfully created

#This function is defined to load one csv table into a table
def load_csv_file(conn, csv_path, table_name):
    """Load one CSV file into a database table"""
    #If the file does not exists a message will be displated and 0 rows will be loaded 
    if not os.path.exists(csv_path):
        print(f"File not found: {csv_path}")
        return 0
    
    #Try will handle the error if any occurs without crashing the program
    try:
        # Reading the CSV file from a detected seperated tab text files
        if csv_path.suffix == ".txt":
            df = pd.read_csv(csv_path, sep="\t")  # Tab-separated files being loaded in the DataFrame
        else:
            df = pd.read_csv(csv_path)  # Loading the regular CSV file
        
        print(f"Reading {csv_path.name}...")

        # SPECIAL HANDLING for datasets_metadata table that is if loading into the datasets_metadata table and the table has a column field convert to string to match the schema
        if table_name == "datasets_metadata" and "columns" in df.columns:
            # Convert columns from int to string to match TEXT column type
            df["columns"] = df["columns"].astype(str)
            print(f"   Converted 'columns' to string type")
        
        # Inserting into database
        df.to_sql(name=table_name, con=conn, if_exists='append', index=False)
        print(f"Loaded {len(df)} rows into '{table_name}' table")
        return len(df)
    #Catches error and then an error message is displayed
    except Exception as e:
        print(f"Error loading {csv_path.name}: {e}")
        return 0

#This functions loads csv files into tables 
def load_all_csv_files(conn):
    """Load all CSV files from the DATA folder"""
    print("\nLooking for CSV files...")
    
    # Go up from app/data to project root, then into the DATA folder
    data_folder = Path(__file__).parent.parent.parent.parent / "DATA"
    print(f"Data folder: {data_folder}") #Printing which folder is being used
    
    # List of files to load
    files_to_load = {
        "users.txt": "users",
        "cyber_incidents.csv": "cyber_incidents",
        "datasets_metadata.csv": "datasets_metadata",
        "it_tickets.csv": "it_tickets"
    }
    
    total_rows = 0
    
    #The for loop , loops over each file and table and then build the full file path to the file
    for filename, table_name in files_to_load.items():
        file_path = data_folder / filename

        #If the file exists the load_csv_file will be called 
        if file_path.exists():
            rows_loaded = load_csv_file(conn, file_path, table_name)
            total_rows += rows_loaded
        else:
            print(f"Skipping {filename} - not found") #Else an message will displayed that file is not found
    
    #This will print the number of rows loaded from the csv
    print(f"\nTotal rows loaded: {total_rows}")
    return total_rows


#Another way of loading the csv
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

#Another way of loading the csv
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

    
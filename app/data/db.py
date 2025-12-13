
import sqlite3 #This works with the SQLite database
from pathlib import Path #This ensures handling file paths

#This is printing where the file is currently at that is its file location
print(f"[DEBUG] Current file location: {Path(__file__).absolute()}")

#Going three levels up from the file location and defining the project root's folder - This is kept in the DATA folder
PROJECT_ROOT = Path(__file__).parent.parent.parent 
print(f"[DEBUG] Project root: {PROJECT_ROOT.absolute()}")

#Creating a path for the folder DATA inside the project root and this is where the databases is stored at
DB_FOLDER = PROJECT_ROOT / "DATA"
print(f"[DEBUG] DB_FOLDER path: {DB_FOLDER.absolute()}")

#Ensuring that the DATA folder exists , exist_ok is preventing errors if the folder is there already
DB_FOLDER.mkdir(exist_ok=True)  
print(f"[DEBUG] DB_FOLDER created/exists: {DB_FOLDER.exists()}")

#Defining a full path for intelligence_platform.db and printing to show where the database is created at
DB_PATH = DB_FOLDER / "intelligence_platform.db"
print(f"[DEBUG] DB_PATH: {DB_PATH.absolute()}")
print(f"[DEBUG] DB will be created at: {DB_PATH.absolute()}\n")

# This function will connect the database and if not exists it will automatically be created
def connect_database(db_path=DB_PATH):
    """
    Connect to the SQLite database.
    If the file doesn't exist, SQLite will create it automatically.
    """
    conn = sqlite3.connect(str(db_path))
    print(f"Connected to database at: {db_path}")
    return conn
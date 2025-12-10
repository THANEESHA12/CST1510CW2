import sqlite3
from pathlib import Path

print(f"[DEBUG] Current file location: {Path(__file__).absolute()}")

# Step 1: Decide where the database file will live
# We'll keep it inside a folder called DATA, next to this project
PROJECT_ROOT = Path(__file__).parent.parent.parent 
print(f"[DEBUG] Project root: {PROJECT_ROOT.absolute()}")

DB_FOLDER = PROJECT_ROOT / "DATA"
print(f"[DEBUG] DB_FOLDER path: {DB_FOLDER.absolute()}")


DB_FOLDER.mkdir(exist_ok=True)  # make sure the folder exists
print(f"[DEBUG] DB_FOLDER created/exists: {DB_FOLDER.exists()}")

DB_PATH = DB_FOLDER / "intelligence_platform.db"
print(f"[DEBUG] DB_PATH: {DB_PATH.absolute()}")
print(f"[DEBUG] DB will be created at: {DB_PATH.absolute()}\n")

# Step 2: Simple function to connect
def connect_database(db_path=DB_PATH):
    """
    Connect to the SQLite database.
    If the file doesn't exist, SQLite will create it automatically.
    """
    conn = sqlite3.connect(str(db_path))
    print(f"Connected to database at: {db_path}")
    return conn



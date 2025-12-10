import bcrypt #This is used for hashing and verifying passwords
from app.data.db import connect_database
from app.data.users import get_user_by_username, insert_user #Functions from users.py are being imported
import sqlite3 

#This function is being defined to register users
def register_user(username, password, role='user'):
    """Register new user with password hashing."""
    conn = connect_database() #Opening a connection to the database
    cursor = conn.cursor() #A cursor is created to run SQL commands

    # The cursor executes and check if user already exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False, f"Username '{username}' already exists."

    #Hash password in plaintext using bcrypt salt
    password_hash = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    
    #Insert into database by calling the function insert_user
    insert_user(username, password_hash, role)
    conn.commit() #Saving the details in the database
    conn.close() #Closing the connection between the database

    return True, f"User '{username}' registered successfully!" #Displaying a message for successfull registration

#A function is being defined to log in user
def login_user(username, password):
    """Authenticate user."""
    conn = connect_database() #Opening a connection to the database
    cursor = conn.cursor() #A cursor is created to run the SQL commands

    #The cursor executes to find user by their username and fetch the row
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close() #Closing the connection between the database

    user = get_user_by_username(username) 
    if not user:
        return False, "User not found."
    
    # Verify password user inputted
    stored_hash = user[2]  # password_hash column
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        return True, f"Login successful!"
    return False, "Incorrect password."

#A function being defined to migrate users from a txt file into the database
def migrate_users_from_file(filepath='DATA/users.txt'):
    """Migrate users from text file to database."""
    # ... migration logic ...
    #This is checking if the users.txt file exists
    if not filepath.exists():
        print(f"File not found: {filepath}")
        print("   No users to migrate.")
        return
    
    cursor = conn.cursor() #A cursor is being created to run SQL commands
    migrated_count = 0

    #Opening the file and going through it line by line
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip() #Empty lines is being skipped
            if not line:
                continue

            # Parse line: username,password_hash
            parts = line.split(',') #Splitting the lines using comma
            #Extracting the hashed passsword and username
            if len(parts) >= 2:
                username = parts[0]
                password_hash = parts[1]

                # Insert user into the database(ignore if already exists) and incrementing if any new row is added as well as catching and printing out any SQLite errors
                try:
                    cursor.execute(
                        "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                        (username, password_hash, 'user')
                    )
                    if cursor.rowcount > 0:
                        migrated_count += 1
                except sqlite3.Error as e:
                    print(f"Error migrating user {username}: {e}")

    conn.commit() #Save changes into the database
    print(f"✅ Migrated {migrated_count} users from {filepath.name}") #Displaying how many users were migrated
    # Verify users were migrated
conn = connect_database() #Opening a connection to the database
cursor = conn.cursor() #A cursor is created to run SQL commands

# Query all users
cursor.execute("SELECT id, username, role FROM users")
users = cursor.fetchall()

#Printing a header with its columns and iterating through users and prinitng them out
print(" Users in database:")
print(f"{'ID':<5} {'Username':<15} {'Role':<10}")
print("-" * 35)
for user in users:
    print(f"{user[0]:<5} {user[1]:<15} {user[2]:<10}")

print(f"\nTotal users: {len(users)}")
conn.close()

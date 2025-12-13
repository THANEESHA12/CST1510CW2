from app.data.db import connect_database #From db the function connect_database is being imported

#This function is being defined to get user by their username
def get_user_by_username(username):
    """Retrieve user by username."""
    conn = connect_database() #Opening a connection to the database
    cursor = conn.cursor() #A cursor is created to run SQL command
    #The cursor executes the SQL command in which a query is selected from the users table
    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )
    user = cursor.fetchone() #This fetches the first matched row or none if the user is not found
    conn.close() #Clsoing the connection to the database
    return user

#This function is being defined to insert new users
def insert_user(username, password_hash, role='user'):
    """Insert new user."""
    conn = connect_database() #Opening a connection to the database
    cursor = conn.cursor() #A cursor is created to run the SQL command
    #The cursor is executing the SQL command
    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role)
    )
    conn.commit() #If new user is inserted, this will save the changes in the database
    conn.close() #Closing the connection to the database
     

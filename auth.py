import bcrypt
import os
import time #used for account lockout 

#Creating a function to hash password using bcrypt
def hashed_password(plain_text_password):
    #Encoding the password to bytes
    password_bytes = plain_text_password.encode('utf-8')
    #Generating a salt by using bcrypt.gensalt()
    salt = bcrypt.gensalt()
    #Hashing password using bcrypt.hashpw()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    #Decoding the hash back to a string to store in a text file
    return hashed_password.decode('utf-8')

#Creating a function that verify the password
def verify_password(plain_text_password, hash_stored):
    #Encoding the plaintext into bytes
    password_bytes = plain_text_password.encode('utf-8')
    #Encoding the stored hash into bytes
    hashed_password_bytes = hash_stored.encode('utf-8')
    #Using bcrypt.checkpw() for password verification + extracting the salt from the hash and comparing
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)

#Defining the user data file as a constant
USER_DATA_FILE = "users.txt"
#A seperate file is being created to track the failed attempts
account_lockout_file = "acc_lockout.txt"

#Creating a function that registers users
def register_user(username, password, role = "user"):
    #Challenge 2 - Registering user with a specific role (user, admin, analyst)
    #Modification made on "login_user" of the file format: username, hashed_password, role
    if role not in ["user", "admin", "analyst"]:
        print("Error: Please enter a valid role")
        return False

    #Checking if the username exists
    if user_exists(username):
        print("Unavailable: Username already taken.")
        return False
    
    #Hashing the password
    hashed_pw = hashed_password(password)
    
    #Appending new user in the file in the format - [username,hashed_password,role]
    with open(USER_DATA_FILE, "a") as f:
        f.write(f"{username},{hashed_pw},{role}\n")

    #Lockout information in here
    with open(account_lockout_file, "a") as f:
        f.write(f"{username},0,0.0\n")

    print(f"Success: {username} account has been registered with role of {role}.")

    #Opening the file and showing all data
    with open(USER_DATA_FILE, "r") as f:
        print("\nUSERS:")
        print(f.read())
    return True


def user_exists(username):
    #Checking if the username already exists 
    try:
        with open(USER_DATA_FILE, "r") as f:
            for line in f: # A line is a record of a user
                data_for_user = line.strip().split(",") # This put the data in this format:- username, hashed_password
                stored_username = data_for_user[0] # This stores the username which will be easier to use for comparison later 

                #Comparing to see if the username exists in the file or not 
                if stored_username == username:
                    return True #username was found against the stored_username
                
    except FileNotFoundError:
        #The file does not exist
        return False #No user in the file
    return False #Username not found in the file



def login_user(username, password):
    #Checking if users are registered 
    file_exists = os.path.exists(USER_DATA_FILE)
    if file_exists == False:
        print("Login Failed: This account is not registered.")
        return False
    
    #Searching for the username in the file
    with open(USER_DATA_FILE, "r") as f:
        for line in f.readlines(): #reading all the lines into the list
            data_for_user= line.strip().split(",") #Using comma to split the format
            if len(data_for_user) == 3:   #role was added for line 76
                user, hash, role = data_for_user
                                                          
            #Verifying username if the username matches
                if user == username:
                    #Checking lockout status firstly then if not lockout check password
                    current_time = time.time()
                    try:
                        with open(account_lockout_file, "r") as locked:
                            for lock_line in locked:
                                stored_username, attempts, locked_time = lock_line.strip().split(",")
                                if stored_username == username:
                                    locked_time = float(locked_time)

                                    #Checking if account is still locked
                                    if current_time < float(locked_time):
                                        print("Login Failed: Your account is locked out.")
                                        return False
                                    elif locked_time != 0.0 and current_time > locked_time:
                                        account_lockout(username, False) #resetting the attempts
                                        print("Try entering password again.")

                    except FileNotFoundError:
                        pass
                    
                    if verify_password(password, hash):
                        print(f"Login successful. Welcome {username}! You are logged in as {role}")
                        account_lockout(username, True)
                        return True
                    else:
                        return account_lockout(username, False)

    #Username not found and loop have finished
    print("Login failed. Please register your account")
    return False

#Creating a function for input validation which validates username format
def validate_username(username):
    #Username validation - should be at least 5 characters long
    if len(username) < 5:
        return False, "Username should contain at least 5 characters."
    
    #Username should contain letters and numbers only
    if not username.isalnum():
        return False, "Username contain only letters and number no spaces or special characters."

    return True, ""

#Creating a function that validate password
def validate_password(password):
    #This will allow to print all the errors user have in there password allowing them to correct them
    error_found = []

    #Password validation - should be 8 characters long
    if len(password) < 8:
        error_found.append("Password must be 8 characters long.")
    
    #Password should have one uppercase character at least
    has_upper = False
    for char in password: #Going through each of the characters in the password
        if char.isupper(): #Checking for uppercase characters
            has_upper = True #An uppercase letter is found
            break #Stop checking as an uppercase character was found

    if not has_upper: #No uppercase characters was found
        error_found.append("Password should contain at least one uppercase letter.")
    
    #Password should have one lowercase character at least
    has_lower = False
    for char in password: #Going through each of the characters in the password
        if char.islower(): #Checking for lowercase characters
            has_lower = True #An lowercase letter is found
            break #Stop checking as an lowercase character was found

    if not has_lower: #No lowercase characters was found
        error_found.append("Password should contain at least one lowercase letter.")
    
    #Password should have one digit at least
    has_digit = False
    for char in password: #Going through each of the characters in the password
        if char.isdigit(): #Checking if the password contain a digit at least
            has_digit = True #A digit is found
            break #Stop checking a digit was found

    if not has_digit: #No digit was found
        error_found.append("Password should contain at least one digit.")
    
    #Password should have at least one special characters
    special_characters = "@#$!" #special characters that can be used
    has_special_characters = False
    for char in password: #Going through each of the characters in the password
        if char in special_characters: #Checking if password contain any of the special_characters
            has_special_characters = True #Password contain special characters
            break #Stop checking as a special characters was found

    if not has_special_characters:
        error_found.append(f"Password should contain at least one special characters - {special_characters}")
    
    #Checking if password has spaces
    has_space = ' ' in password
    if has_space:
        error_found.append("Password should not contain spaces.")

    #Returning all the errors for it to be printed 
    if error_found:
        return False, error_found
    
    return True, []

#Challenge 1 - Checking is password is weak, medium or strength
def check_password_strength(password):
    #Checking for presence of length, uppercase, lowercase, digits and special characters
    count = 0 #This will increment if those requirements are met and this will determine how strong the password is

    if len(password) >= 8:
        count += 1
    if len(password) >= 12:
        count += 1

    has_upper = False 
    for char in password:
        if char.isupper():
            has_upper = True
            break
    if has_upper:
        count += 1

    has_lower = False
    for char in password:
        if char.islower():
            has_lower = True 
            break 
    if has_lower:
        count += 1

    has_digit = False
    for char in password:
        if char.isdigit():
            has_digit = True
            break 
    if has_digit:
        count += 1

    special_characters = "@#$!"
    has_special_characters = False
    for char in password:
        if char in special_characters:
            has_special_characters = True
            break 
    if has_special_characters:
        count += 1

    #Checking length of password to determine if its weak, strong, medium
    if len(password)<8: #use len (length) to check the length of the password, if contain < than 8 character the password is weak
        return "Weak"
    elif len(password) >=8 and len(password)<=12: #if pw is greater or equal to 8 character or less or equal to 12 characters the pw is moderate
        return "Medium"
    else:
        return "Strong" #if pw contain greater or equal to 12 character the pw is strong

      
#Implementing a function that locks account after 3 failed login attempts
def account_lockout(username, success): #Success will inform if the log in was sucessfull or not
    current_time = time.time() #Storing current_time in second
    attempts = 0 #Initialised at 0 and will increment later on depending on the failed attempts
    lockout_time = 0.0 #Demonstrate when the lockout ends

    #Reading data that is currently in the file 
    try:
        with open(account_lockout_file, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = [] #If file does not exists it put lines in an empty list
    
    new_lines=[]
    found = False
    for line in lines: #Looping through each line in the file
        stored_username , stored_attempts, stored_lockout_time = line.strip().split(",") #Splitting username, attempts and lockout_time using comma
        if stored_username == username:
            attempts = int(stored_attempts) #Converting attempts into integer
            lockout_time = float(stored_lockout_time) #Converting lockout_time into float
            found = True
        else:
            new_lines.append(line) #A new user data is kept in a new line to prevent data lost
    
    #Checking that locked out time has passed over the locked account
    if success == False:
            if lockout_time != 0.0 and current_time > lockout_time: #lockout_time is over + resetted
                attempts = 0
                lockout_time = 0.0
                print("Account lockout time terminates. Try again.")
                new_lines.append(f"{username},{attempts},{lockout_time}\n") #Line 278 - 280 save the updated version after the 5 min lockout is finished in file this allow for 3 attempts again before next lockout_time2
                with open(account_lockout_file, "w") as f:
                    f.writelines(new_lines)
                return False


    #If user have successfully log in update attempts and lockout_time 
    if success:
        attempts = 0 #A successful login makes attempts 0 again
        lockout_time = 0.0 #A successful login makes lockout_time 0.0 meaning no waiting time 
    else:
        #If user is on lockout that is failed login
        if current_time < float(lockout_time): #Checking if current_time is less than lockout_time
            print("Login Failed: Account is locked out.") #If yes this message is displayed
            new_lines.append(f"{username},{attempts},{lockout_time}\n")
            with open(account_lockout_file, "w") as f:
                f.writelines(new_lines)
            return False
        
        #Increasing attempts if account not locked yet and applying lockout_time
        attempts += 1
        if attempts >= 3: #lockout_time is added from here 
            convert = 5 * 60 #Converting 5 minutes into seconds
            lockout_time = current_time + convert
            print("Login Failed: Account is locked out for 5 minutes. Please try again later.")
        else:
            print("Login Failed: Password is incorrect.")

        #Saving all the updated information
        new_lines.append(f"{username},{attempts},{lockout_time}\n")
        with open(account_lockout_file, "w") as f:
            f.writelines(new_lines)

        return success
    


def display_menu():
    """Displays the main menu options."""
    print("\n" + "="*50)
    print("  MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print("  Secure Authentication System")
    print("="*50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)

def main():
    """Main program loop."""
    print("\nWelcome to the Week 7 Authentication System!")
    
    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()
        
        if choice == '1':
            # Registration flow
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()
            
            # Validate username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue
            
            password = input("Enter a password: ").strip()

            #Displaying the password strength
            strength = check_password_strength(password)
            print(f"The password strength is: {strength}")
            
            # Validate password
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error in password are: ")
                for error in error_msg:
                    print(">",error)
                continue
            
            # Confirm password
            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue
            
            role = input("What is your role? (user/admin/analyst): ").strip().lower()
            # Register the user
            register_user(username, password,role)
            
        
        elif choice == '2':
            # Login flow
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            
            # Attempt login
            if login_user(username, password):
                print("\nYou are now logged in.")
                print("(In a real application, you would now access the domain")
                
                # Optional: Ask if they want to logout or exit
                input("\nPress Enter to return to main menu...")
        
        elif choice == '3':
            # Exit
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break
        
        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")
            
if __name__ == "__main__":
    main()
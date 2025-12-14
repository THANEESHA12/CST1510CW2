# Week 7: Secure Authentication System
Student Name: Lowtoo Thaneesha
Student ID: M01068106  
Course: CST1510 -CW2 -  Multi-Domain Intelligence Platform 

## Project Description
A command-line authentication system implementing secure password hashing
This system allows users to register accounts and log in with proper pass

## Features
- Secure password hashing using bcrypt with automatic salt generation
- User registration with duplicate username prevention
- User login with password verification
- Input validation for usernames and passwords
- File-based user data persistence

## Technical Implementation
- Hashing Algorithm: bcrypt with automatic salting
- Data Storage: Plain text file (`users.txt`) with comma-separated values
- Password Security: One-way hashing, no plaintext storage
- Validation: Username (5 or greater than 5 alphanumeric character), Password is strong above 12 characters


## Week 8: Data Pipeline (Database migration) and Crud (SQL)
## Project Description
- Implementing crud operations for each of the domains and all the CSV's provided loading them into the intelligence_platform.db

## Features
- Creating 4 database table, one for each - user, cybersecurity, data science and IT operations
- Users are migrated into a users.txt 
- Pandas is used to load all of the CSV which makes the database more cleaner to read

## Technical Operations 
- Using pathlib to import the path of the database and making a connection to it
- Implementing the Analytical Queries that is doing the SQL clauses
- Setting up the complete database in a single function called setup_database_complete

## Week 9 - Setting up the Streamlit

## Project Description
- Streamlit turns Python Scripts into an interactive application
- Contains build in widgets that can be used to implemented the application

## Features
- Implementing bar charts and pie charts for each of the domain according to the database  
- Implementing side bars for better navigation

## Technical Operations
- Using st.button for the creation of all buttons for better navigations
- Implemneting side bars that simplify the navigation along with button in it for user to navigate around the platform
- Using plotly to implemented the charts

## Week 10 - AI Implementation

## Project Description
- Using gemini api key to implement AI which allows user to chat with AI or analyze incidents, datasets or tickets

## Features
- AI analyzer is used to analyse any tickets, datasets or incidents that user select. Thus this provide details about the selected information
- AI assistant is for user to ask questions 

## Technical Implementaion
- Obtaining an API key for Gemini
- Downloading the Google API key extension so thats the AI runs.

## Running instruction
- The main file to run the streamlit is home.py. I have run it this way:- cd CST1510CW2 and the streamlit run streamlit_code/home.py

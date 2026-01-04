import sqlite3
import string
import hashlib

# Validates the username and password and adds them into the database if they are verified
def new_account_verification(username, password):
    special_characters = string.punctuation
    if len(username) < 4:
        return "Create_Account", "Invalid input: username must be 4 or more characters."
    elif len(password) < 4:
        return "Create_Account", "Invalid input: password must be 4 or more characters."
    elif not any(char.isupper() for char in password):
        return "Create_Account", "Invalid password: must contain at least one uppercase letter."
    elif not any(char in special_characters for char in password):
        return "Create_Account", "Invalid password: must contain at least one special character."
    else:
        create_connect = sqlite3.connect('user_details_database.db')
        create_cursor = create_connect.cursor()
    

        # Check if username already exists
        create_cursor.execute("SELECT * FROM user_details WHERE Username = ?", (username,))
        if create_cursor.fetchone():
            create_connect.close()
            return "Create_Account", "Username already exists"
        
        hashed_password = hashlib.sha256(password.encode()).digest()
        

        # Creates new user if the username hasnt been used before
        create_cursor.execute("INSERT INTO user_details (Username, Password) VALUES (?, ?)", (username, hashed_password))
        create_connect.commit()
        create_connect.close()
        return "Chatbot_Page", ""


import sqlite3
import string

# Validates the username and password before checking in the database if they are correct
def existing_account_verification(username, password):
    special_characters = string.punctuation
    if len(username) < 4:
        return "Login_Page", "Invalid input: username must be 4 or more characters."
    elif len(password) < 4:
        return "Login_Page", "Invalid input: password must be 4 or more characters."
    elif not any(char.isupper() for char in password):
        return "Login_Page", "Invalid password: must contain at least one uppercase letter."
    elif not any(char in special_characters for char in password):
        return "Login_Page", "Invalid password: must contain at least one special character."
    else:
        # Check if credentials exist in the user database
        login_connect = sqlite3.connect('user_details_database.db')
        login_cursor = login_connect.cursor()

        login_cursor.execute("SELECT * FROM user_details WHERE Username = ?", (username,))
        result = login_cursor.fetchone()
        login_connect.close()

        if result:
            stored_password = result[1]
            if password == stored_password:
                return "Chatbot_Page", "", username  # Takes user to main page if login successful
            else:
                return "Login_Page", "Incorrect username or password"
        else:
            return "Login_Page", "Incorrect username or password"

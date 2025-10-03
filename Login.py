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

        global current_username
        if result:
            stored_password = result[1]
            if password == stored_password:
                current_username = username # Sets logged in username
                return "Chatbot_Page", ""   # Takes user to main page if login successful
            else:
                return "Login_Page", "Incorrect username or password"
        else:
            return "Login_Page", "Incorrect username or password"

# Validates the username and password and adds them into the database if they are verified
def new_account_verification(username, password):
    special_characters = "!@#$%^&*()_+-=[]{}|;:',.<>?/~`"
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
        

        # Create new user
        create_cursor.execute("INSERT INTO user_details (Username, Password) VALUES (?, ?)", (username, password))
        create_connect.commit()
        create_connect.close()
        return "Chatbot_Page", ""

 # Pages
    if game_state == "Login_Page":
        text_line("BioBot", FONT, WHITE, 520, 60)
        text_line("Login", SMALL_FONT, WHITE, 555, 140)

        # Display username in the button 
        button_text_username = username if username or typing == "username" else "Username"

        # Display password or * in the button
        if show_password_flag:
            button_text_password = password if password or typing == "password" else "Password"
        else:
            button_text_password = "*" * len(password) if password or typing == "password" else "Password"

        # Draw buttons where username and password can be entered
        clickable_button(button_text_username, username_input_box, DARK_GREEN, WHITE)
        clickable_button(button_text_password, password_input_box, DARK_GREEN, WHITE)

        if show_password_flag:
            button_writing = "Hide"
        else:
            button_writing = "Show"
        clickable_button(button_writing, show_password_box, DARK_GREEN, WHITE)  # Button to show the password

        login_pressed = clickable_button("Login", login_box, DARK_GREEN, WHITE)
        create_account_nav_pressed = clickable_button("Create Account", create_box, DARK_GREEN, WHITE)

        # Display error message saying what the error is if username or password is invalid
        if error_message:
            text_line(error_message, ERROR_FONT, RED, 420, 500)

        # Verify if login is correct
        if login_pressed and (current_time - last_click_time > CLICK_DELAY):
            game_state, error_message = existing_account_verification(username, password)
            last_click_time = current_time

        # Change to create account page
        if create_account_nav_pressed and (current_time - last_click_time > CLICK_DELAY):
            username = ""
            password = ""
            error_message = ""
            game_state = "Create_Account"
            last_click_time = current_time

    elif game_state == "Create_Account":
        text_line("BioBot", FONT, WHITE, 520, 60)
        text_line("Account Creation", SMALL_FONT, WHITE, 500, 140)

        button_text_username = username if username or typing == "username" else "Username"
        if show_password_flag:
            button_text_password = password if password or typing == "password" else "Password"
        else:
            button_text_password = "*" * len(password) if password or typing == "password" else "Password"

        # Draw input buttons
        clickable_button(button_text_username, username_input_box, DARK_GREEN, WHITE)
        clickable_button(button_text_password, password_input_box, DARK_GREEN, WHITE)

        if show_password_flag:
            button_writing = "Hide"
        else:
            button_writing = "Show"
        clickable_button(button_writing, show_password_box, DARK_GREEN, WHITE)

        create_account_pressed = clickable_button("Create Account", create_account_submit_box, DARK_GREEN, WHITE)
        back_to_login_pressed = clickable_button("Back to Login", create_box, DARK_GREEN, WHITE)

        if error_message:
            text_line(error_message, ERROR_FONT, RED, 420, 500)

        # Verify if account creation is correct
        if create_account_pressed and (current_time - last_click_time > CLICK_DELAY):
            game_state, error_message = new_account_verification(username, password)
            last_click_time = current_time

        # Change to login page
        if back_to_login_pressed and (current_time - last_click_time > CLICK_DELAY):
            username = ""
            password = ""
            error_message = ""
            typing = None
            game_state = "Login_Page"
            last_click_time = current_time

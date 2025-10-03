import pygame
import sys
import sqlite3
import string
import csv
import random
import difflib


# Tracks what page the user is on
game_state = "Login_Page"

# Typing and login logic 
typing = None
username = ""
password = ""
error_message = ""

# Toggles if password is visable
show_password_flag = False



# Stores the users confidence for the flashcards
def set_confidence(term, RAG):
    user_flashcard_confidence[term] = RAG

# Stores XP user has gained into the user details database
def xp_system(username, points_gained):
    xp_database_connection = sqlite3.connect('user_details_database.db') # Opens the user detail database
    xp_cursor = xp_database_connection.cursor()

    # Retrieves the current XP in the database
    xp_cursor.execute("SELECT XP FROM user_details WHERE Username = ?", (username,))
    xp_result = xp_cursor.fetchone()
    if xp_result:
        current_xp = xp_result[0]
    else:
        current_xp = 0
        # Updates XP if XP is gained
    new_xp = current_xp + points_gained
    xp_cursor.execute("UPDATE user_details SET XP = ? WHERE Username = ?", (new_xp, username))
    xp_database_connection.commit()
    xp_database_connection.close()

# Leveling up system and how much XP is required to level up
def level_up_system(xp):
    level_thresholds = [0, 100, 250, 500, 1000, 5000, 10000] # Each threshold for XP levels

    # Determines user level based on their XP 
    level = 1
    for i in level_thresholds:
        if xp>= i:
            level = level + 1
        else:
            break
    return level - 1

# Calculate RAG confidence counts from flashcards 
def RAG_scores():
    red = 0
    amber = 0
    green = 0
    for level in user_flashcard_confidence.values():
        if level == 1:
            red = red + 1
        elif level == 2:
            amber = amber + 1
        elif level == 3:
            green = green + 1
    return red, amber, green

# Retreives the definition for the term the user asks for 
def biology_term_definition(collect_biology_term):
    clear_terms = blacklist_fillers(collect_biology_term) # Removes all of the blacklisted words from the user question
    terms = [term.lower() for term, _ in biology_notes]

    # Try exact match first
    for term, definition in biology_notes:
        if term.lower() == clear_terms:
            return definition
    
    # If no exact match, find closest match using difflib
    closest_matches = difflib.get_close_matches(clear_terms, terms, n=1, cutoff=0.6) # If the entered phrase is more than 60% correct it will return that definition
    if closest_matches:
        # Get index of closest match
        closest_term = closest_matches[0]
        for term, definition in biology_notes:
            if term.lower() == closest_term:
                return f"{definition}"
            
    
    return "Sorry, I couldn't find that term."

def xp_popup_animation(amount): # When the user completes a flashcard or asks the chatbot a question a xp pop-up appears
    global xp_popup_text, xp_popup_start_time
    xp_popup_text = f"+{amount} XP"
    xp_popup_start_time = pygame.time.get_ticks()

# Removes any common words like the so sorting questions is more managable
def blacklist_fillers(user_input):
    filler_words = {"what", "is", "the", "a", "an", "define", "meaning", "of", "please"} # Words to be excluded from the search
    words_entered = user_input.lower().split()
    filtered_words = [word for word in words_entered if word not in filler_words]
    return "".join(filtered_words)



# Main game loop

running = True
while running:
    screen.fill(LIGHT_GREEN)  # Sets background colour
    current_time = pygame.time.get_ticks() # Stops user from repeatidly clicking with a delay

    # Event handling loops
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Detects if mouse has been pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            if username_input_box.collidepoint(event.pos):
                typing = "username" # User begins to type in username box
                error_message = ""
            elif password_input_box.collidepoint(event.pos):
                typing = "password" # User begins to type in password box
                error_message = ""
            elif show_password_box.collidepoint(event.pos):
                show_password_flag = not show_password_flag  # Toggle if password is visable
            elif game_state == "Chatbot_Page" and chatbot_user_typing_box.collidepoint(event.pos):
                typing = "chatbot_input"
            else:
                typing = None  # Typing stops if user clicks outside button

        # Typing logic
        if event.type == pygame.KEYDOWN:
            if typing == "username":
                if event.key == pygame.K_RETURN: # Typing stops if user presses enter key
                    typing = None
                elif event.key == pygame.K_BACKSPACE: # Deletes last character if backspace is clicked
                    username = username[:-1]
                else:
                    username += event.unicode # Allows for characters to be added to username

            elif typing == "password":
                if event.key == pygame.K_RETURN:
                    typing = None
                elif event.key == pygame.K_BACKSPACE:
                    password = password[:-1]
                else:
                    password += event.unicode # Allows for characters to be added to password

            elif typing == "chatbot_input":
                if event.key == pygame.K_RETURN:
                    chatbot_message = biology_term_definition(chatbot_user_typing_text.strip()) # Searches for definition given by user in biology database
                    chatbot_user_typing_text = "" # Clears input box once message has been sent
                    xp_system(current_username, 20) # User gains XP for asking chatbot question
                    xp_popup_animation(20)
                elif event.key == pygame.K_BACKSPACE:
                    chatbot_user_typing_text = chatbot_user_typing_text[:-1] # Removes last character from textbox
                else:
                    chatbot_user_typing_text += event.unicode # Allows for characters to be added to textbox
                    

        # Page changes if option on sidebar is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            if choose_chatbot_box.collidepoint(event.pos):
                game_state = "Chatbot_Page"
            if choose_flashcards_box.collidepoint(event.pos):
                game_state = "Flashcards_Page"
            if choose_performance_box.collidepoint(event.pos):
                game_state = "Performance_Page"

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

    elif game_state == "Chatbot_Page":
        main_pages_layout()
        text_line("CHATBOT", FONT, BLACK, 500, 10)
        pygame.draw.rect(screen, WHITE, chatbot_user_typing_box, 0)  # Filled white box
        pygame.draw.rect(screen, BLACK, chatbot_user_typing_box, 2)  # Black border

        if chatbot_user_typing_text == "" and typing != "chatbot_input":
            chatbot_placeholder_text = SMALL_FONT.render("Ask anything...", True, GREY)
            screen.blit(chatbot_placeholder_text, (chatbot_user_typing_box.x + 10, chatbot_user_typing_box.y + 10))
        else:
            input_text_surface = SMALL_FONT.render(chatbot_user_typing_text, True, BLACK)
            screen.blit(input_text_surface, (chatbot_user_typing_box.x + 10, chatbot_user_typing_box.y + 10))

        pygame.draw.rect(screen, WHITE, chatbot_message_box)
        pygame.draw.rect(screen, BLACK, chatbot_message_box, 2)
        text_line(chatbot_message, SMALL_FONT, BLACK, 280, 120)

    elif game_state == "Flashcards_Page":
        main_pages_layout()
        text_line("FLASHCARDS", FONT, BLACK, 500, 10)
        pygame.draw.rect(screen, WHITE, (260, 80, 800, 600))

        if current_flashcard:
            if show_flashcard_answer:
                # Show the flashcard answer
                text_line("Answer:", FONT, BLACK, 320, 100)
                text_line(current_flashcard[1], SMALL_FONT, BLACK, 320, 150)
            else:
                # Show the flashcard question/ Key term
                text_line("Term:", FONT, BLACK, 320, 100)
                text_line(current_flashcard[0], SMALL_FONT, BLACK, 320, 150)
        else:
            text_line("Click 'Next' to start revision!", SMALL_FONT, BLACK, 400, 300)

        # Flip and Next buttons
        flip_button = pygame.Rect(350, 550, 200, 60)
        next_button = pygame.Rect(650, 550, 200, 60)

        if clickable_button("Flip", flip_button, DARK_GREEN, WHITE) and (current_time - last_click_time > CLICK_DELAY):
            show_flashcard_answer = not show_flashcard_answer
            last_click_time = current_time

        if clickable_button("Next", next_button, DARK_GREEN, WHITE) and (current_time - last_click_time > CLICK_DELAY):
            current_flashcard = random.choice(biology_notes)
            show_flashcard_answer = False
            flashcard_xp_awarded = False
            last_click_time = current_time

        if current_flashcard and show_flashcard_answer:

            # RAG buttons

            red_flashcard_button = pygame.Rect(350, 330, 100, 50)
            amber_flashcard_button = pygame.Rect(500, 330, 100, 50)
            green_flashcard_button = pygame.Rect(650, 330, 100, 50)

            if clickable_button("Red", red_flashcard_button, RED, WHITE) and (current_time - last_click_time > CLICK_DELAY):
                set_confidence(current_flashcard[0], 1)  # Level 1 - RED
                if not flashcard_xp_awarded:
                    xp_system(current_username, 2)
                    xp_popup_animation(2)
                    flashcard_xp_awarded = True
                last_click_time = current_time

            if clickable_button("Amber", amber_flashcard_button, (255, 191, 0), WHITE) and (current_time - last_click_time > CLICK_DELAY):
                set_confidence(current_flashcard[0], 2)  # Level 2 - AMBER
                if not flashcard_xp_awarded:
                    xp_system(current_username, 5)
                    xp_popup_animation(5)
                    flashcard_xp_awarded = True
                last_click_time = current_time

            if clickable_button("Green", green_flashcard_button, LIGHT_GREEN, WHITE) and (current_time - last_click_time > CLICK_DELAY):
                set_confidence(current_flashcard[0], 3)  # Level 3 - GREEN
                if not flashcard_xp_awarded:
                    xp_system(current_username, 10)
                    xp_popup_animation(10)
                    flashcard_xp_awarded = True
                last_click_time = current_time
            

    elif game_state == "Performance_Page":
        main_pages_layout()
        text_line("PERFORMANCE", FONT, BLACK, 500, 10)

        red, amber, green = RAG_scores()
        text_line(f"Red: {red}", SMALL_FONT, RED, 300, 200)
        text_line(f"Amber: {amber}", SMALL_FONT, (255, 191, 0), 300, 250)
        text_line(f"Green: {green}", SMALL_FONT, DARK_GREEN, 300, 300)


    elif game_state == "Settings_Page":
        screen.fill(LIGHT_GREEN)
        pygame.draw.rect(screen, WHITE, (260, 80, 800, 600))
        
        
        


    pygame.display.flip() # Update screen

# Quit pygame
pygame.quit()
sys.exit()

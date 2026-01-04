import pygame
from database.setup_database import setup_database
from auth.login import existing_account_verification
from auth.create_account import new_account_verification
from ui.config import *
from ui.login_create_ui import login_page, create_account_page
from ui.layout import main_pages_layout
from logic.chatbot_logic import biology_term_definition
from ui.chatbot_ui import chatbot_page
from ui.flashcard_ui import flashcards_page
from logic.xp_system import xp_system, xp_popup_animation
from ui.performance_ui import performance_page
from logic.streak_system import update_streak

# Main code for my Biology revision app 
def main():
    pygame.init() # Starts pygame 
    screen = pygame.display.set_mode((1200, 800)) # Creates the screen size
    pygame.display.set_caption("BioBot")

    biology_notes = setup_database()  # Ensure Databases exist

    game_state = "Login_Page" # Sets the first page the user is on to the login page

    # Typing and Login logic
    typing = None 
    username = ""
    password = ""
    error_message = ""
    last_click_time = 0
    show_password_flag = False # Toggles if password is visible 
    current_username = ""
    current_streak = 0

    # Button settings for the login and create account page 
    username_input_box = pygame.Rect(450, 250, 300, 60)
    password_input_box = pygame.Rect(450, 330, 300, 60)
    show_password_box = pygame.Rect(790, 330, 100, 60)
    login_box = pygame.Rect(450, 420, 300, 60)
    create_box = pygame.Rect(850, 700, 300, 60)
    create_account_submit_box = pygame.Rect(450, 420, 300, 60)

    # Chatbot message settings
    chatbot_user_typing_box = pygame.Rect(260, 700, 600, 50)
    chatbot_message_box = pygame.Rect(270, 110, 860, 60)
    chatbot_user_typing_text = ""
    chatbot_message = ""
    recent_questions = []


    # Settings for flashcard page 
    current_flashcard = None
    show_flashcard_answer = False
    flashcard_xp_awarded = False 

    # Setting to allow XP popup to be visible
    xp_popup_text = ""
    xp_popup_start_time = 0

    # Motivational quote for the performance page 
    performance_quote = ""

    # Main code function
    running = True
    while running:
        screen.fill(LIGHT_GREEN)  # Sets background colour
        current_time = pygame.time.get_ticks() # Creates a time delay so users can not rapidly click

        # Event handling loops
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Detects if mouse has been pressed
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if username_input_box.collidepoint(event.pos):
                    typing = "username" # User starts typing username in username box
                    error_message = ""
                elif password_input_box.collidepoint(event.pos):
                    typing = "password" # User starts typing password in password box 
                    error_message = ""
                elif show_password_box.collidepoint(event.pos):
                    show_password_flag = not show_password_flag  # Toggle if password is visable
                elif game_state == "Chatbot_Page" and chatbot_user_typing_box.collidepoint(event.pos):
                    typing = "chatbot_input"
                else:
                    typing = None  # Typing stops if user clicks outside the button

            # Typing logic
            if event.type == pygame.KEYDOWN:
                if typing == "username":
                    if event.key == pygame.K_RETURN: # Typing stops and is submitted if user presses enter key
                        typing = None
                    elif event.key == pygame.K_BACKSPACE: # Deletes last character if backspace is clicked
                        username = username[:-1]
                    else:
                        username += event.unicode # Allows for any characters to be added to username

                elif typing == "password":
                    if event.key == pygame.K_RETURN:
                        typing = None
                    elif event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    else:
                        password += event.unicode # Allows for any characters to be added to password

                elif typing == "chatbot_input":
                    if event.key == pygame.K_RETURN:
                        user_question = chatbot_user_typing_text.strip()
                        chatbot_message = biology_term_definition(user_question)
                        chatbot_user_typing_text = ""

                        # Adds most recent question to the list 
                        recent_questions.append(user_question)

                        # Ensures that the list size isnt over 5 
                        if len(recent_questions) > 5:
                            recent_questions.pop(0)

                        xp_system(current_username, 20) # User gains XP for asking chatbot question

                        #XP popup systen
                        xp_popup_text, xp_popup_start_time = xp_popup_animation(20, xp_popup_text, xp_popup_start_time)
                    elif event.key == pygame.K_BACKSPACE:
                        chatbot_user_typing_text = chatbot_user_typing_text[:-1] # Removes last character from textbox
                    else:
                        chatbot_user_typing_text += event.unicode # Allows for characters to be added to textbox
                 
                    
        if game_state == "Login_Page":
            game_state, username, password, error_message, last_click_time = login_page(
            screen, username, password, typing, show_password_flag, error_message,
            username_input_box, password_input_box, show_password_box,
            login_box, create_box, game_state, current_time, last_click_time
        )
            if game_state == "Chatbot_Page":  # If login was successful
                current_username = username
                current_streak = update_streak(current_username)

        elif game_state == "Create_Account":
            game_state, username, password, error_message, last_click_time = create_account_page(
            screen, username, password, typing, show_password_flag, error_message,
            username_input_box, password_input_box, show_password_box,
            create_account_submit_box, create_box, game_state, current_time, last_click_time
        )
            if game_state == "Chatbot_Page":  # If creating account was successful
                current_username = username
                current_streak = update_streak(current_username)

        elif game_state == "Chatbot_Page": 
            chatbot_message = chatbot_page(screen, typing, chatbot_user_typing_box, chatbot_message_box, game_state, chatbot_user_typing_text, chatbot_message, current_username, recent_questions)

        elif game_state == "Flashcards_Page":
             last_click_time, current_flashcard, show_flashcard_answer, flashcard_xp_awarded, xp_popup_text, xp_popup_start_time = flashcards_page(
                 screen, biology_notes, current_time, last_click_time, current_username, game_state,
        current_flashcard, show_flashcard_answer, flashcard_xp_awarded, xp_popup_text, xp_popup_start_time
    )

        elif game_state == "Performance_Page":
            performance_quote = performance_page(game_state, screen, current_username, biology_notes, current_streak, performance_quote)
        
        # Creates a default main page for chatbot flashcard and performance page 
        if game_state in ["Chatbot_Page", "Flashcards_Page", "Performance_Page"]:
            chatbot_clicked, flashcards_clicked, performance_clicked, logout_clicked = main_pages_layout(game_state, screen, current_username)
            

            # Sidebar functionality 
            if chatbot_clicked:
                game_state = "Chatbot_Page"
            elif flashcards_clicked:
                game_state = "Flashcards_Page"
            elif performance_clicked:
                game_state = "Performance_Page"
            elif logout_clicked: 
                game_state = "Login_Page"
                username = ""
                password = ""
                current_username = ""
                
        # XP Popup display logic
        if xp_popup_text and pygame.time.get_ticks() - xp_popup_start_time < 2000:
            text_line(screen, xp_popup_text, SMALL_FONT, DARK_GREEN, 900, 60)

        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()

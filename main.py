import pygame
from database.setup_database import setup_database
from auth.login import existing_account_verification
from auth.create_account import new_account_verification
from ui.config import *
from ui.login_create_ui import login_page, create_account_page
from ui.layout import main_pages_layout

pygame.init()

def main():
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("BioBot")

    setup_database()  # Ensure DBs exist


    game_state = "Login_Page"

    # Typing and Login logic
    typing = None 
    username = ""
    password = ""
    error_message = ""
    last_click_time = 0
    # Toggles if password is visible 
    show_password_flag = False

    # Button settings - Buttons for login page
    username_input_box = pygame.Rect(450, 250, 300, 60)
    password_input_box = pygame.Rect(450, 330, 300, 60)
    show_password_box = pygame.Rect(790, 330, 100, 60)
    login_box = pygame.Rect(450, 420, 300, 60)
    create_box = pygame.Rect(850, 700, 300, 60)
    create_account_submit_box = pygame.Rect(450, 420, 300, 60)

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
                #elif game_state == "Chatbot_Page" and chatbot_user_typing_box.collidepoint(event.pos):
                    #typing = "chatbot_input"
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

        if game_state == "Login_Page":
            game_state, username, password, error_message, last_click_time = login_page(
            screen, username, password, typing, show_password_flag, error_message,
            username_input_box, password_input_box, show_password_box,
            login_box, create_box, game_state, current_time, last_click_time
        )

        elif game_state == "Create_Account":
            game_state, username, password, error_message, last_click_time = create_account_page(
            screen, username, password, typing, show_password_flag, error_message,
            username_input_box, password_input_box, show_password_box,
            create_account_submit_box, create_box, game_state, current_time, last_click_time
        )

                #elif typing == "chatbot_input":
                    #if event.key == pygame.K_RETURN:
                        #chatbot_message = biology_term_definition(chatbot_user_typing_text.strip()) # Searches for definition given by user in biology database
                        #chatbot_user_typing_text = "" # Clears input box once message has been sent
                        #xp_system(current_username, 20) # User gains XP for asking chatbot question
                        #xp_popup_animation(20)
                    #elif event.key == pygame.K_BACKSPACE:
                        #chatbot_user_typing_text = chatbot_user_typing_text[:-1] # Removes last character from textbox
                    #else:
                        #chatbot_user_typing_text += event.unicode # Allows for characters to be added to textbox
                    

    # --- Sidebar layout and clicks ---
        if game_state in ["Chatbot_Page", "Flashcards_Page", "Performance_Page"]:
            chatbot_clicked, flashcards_clicked, performance_clicked = main_pages_layout(game_state, screen)

            if chatbot_clicked:
                game_state = "Chatbot_Page"
            elif flashcards_clicked:
                game_state = "Flashcards_Page"
            elif performance_clicked:
                game_state = "Performance_Page"

        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()


  


    pygame.display.flip() # Update screen

# Quit pygame
pygame.quit()
sys.exit()

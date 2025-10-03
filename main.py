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

  


    pygame.display.flip() # Update screen

# Quit pygame
pygame.quit()
sys.exit()

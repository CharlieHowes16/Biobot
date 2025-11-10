import pygame
from auth.login import existing_account_verification
from auth.create_account import new_account_verification
from ui.config import *

def login_page(screen, username, password, typing, show_password_flag, error_message,
               username_input_box, password_input_box, show_password_box, 
               login_box, create_box, game_state, current_time, last_click_time):

    text_line(screen, "BioBot", FONT, WHITE, 520, 60)
    text_line(screen, "Login", SMALL_FONT, WHITE, 555, 140)

    button_text_username = username if username or typing == "username" else "Username"

    if show_password_flag:
        button_text_password = password if password or typing == "password" else "Password"
    else:
        button_text_password = "*" * len(password) if password or typing == "password" else "Password"

    clickable_button(screen, button_text_username, username_input_box, DARK_GREEN, WHITE)
    clickable_button(screen, button_text_password, password_input_box, DARK_GREEN, WHITE)

    button_writing = "Hide" if show_password_flag else "Show"
    clickable_button(screen, button_writing, show_password_box, DARK_GREEN, WHITE)

    login_pressed = clickable_button(screen, "Login", login_box, DARK_GREEN, WHITE)
    create_account_nav_pressed = clickable_button(screen, "Create Account", create_box, DARK_GREEN, WHITE)

    if error_message:
        text_line(screen, error_message, ERROR_FONT, RED, 420, 500)

    if login_pressed and (current_time - last_click_time > CLICK_DELAY):
        game_state, error_message, username  = existing_account_verification(username, password)
        last_click_time = current_time

    if create_account_nav_pressed and (current_time - last_click_time > CLICK_DELAY):
        username, password, error_message = "", "", ""
        game_state = "Create_Account"
        last_click_time = current_time

    return game_state, username, password, error_message, last_click_time


def create_account_page(screen, username, password, typing, show_password_flag, error_message,
                        username_input_box, password_input_box, show_password_box,
                        create_account_submit_box, create_box, game_state, current_time, last_click_time):

    text_line(screen, "BioBot", FONT, WHITE, 520, 60)
    text_line(screen, "Account Creation", SMALL_FONT, WHITE, 500, 140)

    button_text_username = username if username or typing == "username" else "Username"

    if show_password_flag:
        button_text_password = password if password or typing == "password" else "Password"
    else:
        button_text_password = "*" * len(password) if password or typing == "password" else "Password"

    clickable_button(screen, button_text_username, username_input_box, DARK_GREEN, WHITE)
    clickable_button(screen, button_text_password, password_input_box, DARK_GREEN, WHITE)

    button_writing = "Hide" if show_password_flag else "Show"
    clickable_button(screen, button_writing, show_password_box, DARK_GREEN, WHITE)

    create_account_pressed = clickable_button(screen, "Create Account", create_account_submit_box, DARK_GREEN, WHITE)
    back_to_login_pressed = clickable_button(screen, "Back to Login", create_box, DARK_GREEN, WHITE)

    if error_message:
        text_line(screen, error_message, ERROR_FONT, RED, 420, 500)

    if create_account_pressed and (current_time - last_click_time > CLICK_DELAY):
        game_state, error_message = new_account_verification(username, password)
        last_click_time = current_time

    if back_to_login_pressed and (current_time - last_click_time > CLICK_DELAY):
        username, password, error_message, typing = "", "", "", None
        game_state = "Login_Page"
        last_click_time = current_time

    return game_state, username, password, error_message, last_click_time

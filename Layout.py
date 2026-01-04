import pygame
import sqlite3
from ui.config import *
from logic.xp_system import level_up_system


# Creates a sidebar for the main page 
choose_chatbot_box = pygame.Rect(0, 200, 175, 60)
choose_flashcards_box = pygame.Rect(0, 300, 175, 60)
choose_performance_box = pygame.Rect(0, 400, 175, 60)
choose_logout_box = pygame.Rect(0, 750, 175, 60)

def main_pages_layout(game_state, screen, current_username):
    pygame.draw.rect(screen, DARK_GREEN, (0, 0, 175, 800))
    text_line(screen, "BioBot", FONT, WHITE, 15, 30)
    # User is able to change between pages when sidebar is clicked
    chatbot_clicked = clickable_button (screen, "Chatbot", choose_chatbot_box, WHITE if game_state == "Chatbot_Page" else DARK_GREEN, GREEN)
    flashcards_clicked = clickable_button (screen, "Flashcards", choose_flashcards_box, WHITE if game_state == "Flashcards_Page" else DARK_GREEN, GREEN)
    performance_clicked = clickable_button (screen, "Performance", choose_performance_box, WHITE if game_state == "Performance_Page" else DARK_GREEN, GREEN)
    logout_clicked = clickable_button (screen, "Logout", choose_logout_box, WHITE if game_state == "Login_Page" else DARK_GREEN, GREEN)

    if current_username:
        xp_database_connection = sqlite3.connect('user_details_database.db')
        xp_cursor = xp_database_connection.cursor()
        xp_cursor.execute("SELECT XP FROM user_details WHERE Username = ?", (current_username,))
        xp_result = xp_cursor.fetchone()
        xp_database_connection.close()
        if xp_result:
            current_xp = xp_result[0]
            level = level_up_system(current_xp)
            text_line(screen, f"XP: {current_xp}  Level: {level}", SMALL_FONT, BLACK, 900, 20)


    return chatbot_clicked, flashcards_clicked, performance_clicked, logout_clicked 

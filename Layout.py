def main_pages_layout():
    screen.fill(LIGHT_GREEN)
    pygame.draw.rect(screen, DARK_GREEN, (0, 0, 175, 800))
    text_line("BioBot", FONT, WHITE, 15, 30)
    chatbot_clicked = clickable_button ("Chatbot", choose_chatbot_box, WHITE if game_state == "Chatbot_Page" else DARK_GREEN, GREEN)
    flashcards_clicked = clickable_button ("Flashcards", choose_flashcards_box, WHITE if game_state == "Flashcards_Page" else DARK_GREEN, GREEN)
    performance_clicked = clickable_button ("Performance", choose_performance_box, WHITE if game_state == "Performance_Page" else DARK_GREEN, GREEN)
    if current_username:
        xp_database_connection = sqlite3.connect('user_details_database.db')
        xp_cursor = xp_database_connection.cursor()
        xp_cursor.execute("SELECT XP FROM user_details WHERE Username = ?", (current_username,))
        xp_result = xp_cursor.fetchone()
        xp_database_connection.close()
        if xp_result:
            current_xp = xp_result[0]
            level = level_up_system(current_xp)
            text_line(f"XP: {current_xp}  Level: {level}", SMALL_FONT, BLACK, 900, 20)
            if xp_popup_text and pygame.time.get_ticks() - xp_popup_start_time < 1000:
                text_line(xp_popup_text, SMALL_FONT, BLACK, 900, 60)

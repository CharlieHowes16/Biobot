# Flashcard and confidence tracking
current_flashcard = None
show_flashcard_answer = False
user_flashcard_confidence = {}
flashcard_xp_awarded = False
current_username = ""

# Stores the users confidence for the flashcards
def set_confidence(term, RAG):
    user_flashcard_confidence[term] = RAG

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

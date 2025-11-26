import pygame
from ui.config import *
from ui.layout import main_pages_layout
from logic.flashcard_logic import current_flashcard, show_flashcard_answer, flashcard_xp_awarded, get_random_flashcard, set_confidence
from logic.xp_system import *

def flashcards_page(screen, biology_notes, current_time, last_click_time, current_username, game_state):
    global current_flashcard, show_flashcard_answer, flashcard_xp_awarded

    # Draw page layout and title for flashcard page 
    main_pages_layout(game_state, screen)
    text_line(screen, "FLASHCARDS", FONT, BLACK, 500, 10)
    pygame.draw.rect(screen, WHITE, (260, 80, 800, 600))

    # Display current flashcard content
    if current_flashcard:
        if show_flashcard_answer:
            # Show the definition
            text_line(screen, "Definition :", FONT, BLACK, 320, 100)
            wrapped_definition = text_wrapping(current_flashcard[1], 50)  # 50 is the maximum amount of characters on one line 
            start_height = 150 # Starting height of the first line in the answer 
            line_height = SMALL_FONT.get_height() # Height of one line of small font text 
        
            for line in wrapped_definition.split('\n'):
                wrapped_small_font = SMALL_FONT.render(line, True, BLACK)
                screen.blit(wrapped_small_font, (320, start_height))
                start_height += line_height
        else:
            # Show the term
            text_line(screen, "Term:", FONT, BLACK, 320, 100)
            text_line(screen, current_flashcard[0], SMALL_FONT, BLACK, 320, 150)
    else:
        # If next is clicked the first flashcard is revealed 
        text_line(screen, "Click 'Next' to start revision!", SMALL_FONT, BLACK, 400, 300)

    # Flashcard control buttons
    flip_button = pygame.Rect(350, 550, 200, 60)
    next_button = pygame.Rect(650, 550, 200, 60)

    # Button to flip flashcard and reveal the definition 
    if clickable_button(screen, "Flip", flip_button, DARK_GREEN, WHITE) and (current_time - last_click_time > CLICK_DELAY):
        show_flashcard_answer = not show_flashcard_answer
        return current_time 

    # Button to get a new flashcard
    if clickable_button(screen, "Next", next_button, DARK_GREEN, WHITE) and (current_time - last_click_time > CLICK_DELAY):
        current_flashcard = get_random_flashcard(biology_notes)
        return current_time 

    # Show confidence rating buttons when answer is revealed
    if current_flashcard and show_flashcard_answer:
        confidence_buttons(screen, current_time, last_click_time, current_username)
    
    return last_click_time 

def confidence_buttons(screen, current_time, last_click_time, current_username):

    # Create RAG rating buttons
    red_button = pygame.Rect(350, 330, 100, 50)
    amber_button = pygame.Rect(500, 330, 100, 50)
    green_button = pygame.Rect(650, 330, 100, 50)

    # Red button for 2 XP 
    if clickable_button(screen, "Red", red_button, RED, WHITE) and (current_time - last_click_time > CLICK_DELAY):
        set_confidence(current_flashcard[0], 1)
        award_flashcard_xp(current_username, 2)
        return current_time

    # Amber button for 5 XP
    if clickable_button(screen, "Amber", amber_button, (255, 191, 0), WHITE) and (current_time - last_click_time > CLICK_DELAY):
        set_confidence(current_flashcard[0], 2)
        award_flashcard_xp(current_username, 5)
        return current_time

    # Green button for 10 XP
    if clickable_button(screen, "Green", green_button, LIGHT_GREEN, WHITE) and (current_time - last_click_time > CLICK_DELAY):
        set_confidence(current_flashcard[0], 3)
        award_flashcard_xp(current_username, 10)
        return current_time
    
    return last_click_time

def award_flashcard_xp(username, xp_amount):
    global flashcard_xp_awarded
    if not flashcard_xp_awarded:
        xp_system(username, xp_amount)
        xp_popup_animation(xp_amount)
        flashcard_xp_awarded = True

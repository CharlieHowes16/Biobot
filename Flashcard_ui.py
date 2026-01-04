import pygame
from ui.config import *
from ui.layout import main_pages_layout
from logic.flashcard_logic import *
from logic.xp_system import *

def flashcards_page(screen, biology_notes, current_time, last_click_time, current_username, game_state, 
                    current_flashcard, show_flashcard_answer, flashcard_xp_awarded, xp_popup_text, xp_popup_start_time):

    # Draw page layout and title for flashcard page 
    main_pages_layout(game_state, screen, current_username)
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
        
            # Wrapping flashcard definitions so they can be fully read
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
        last_click_time = current_time
        return last_click_time, current_flashcard, show_flashcard_answer, flashcard_xp_awarded, xp_popup_text, xp_popup_start_time  

    # Button to get a new flashcard
    if clickable_button(screen, "Next", next_button, DARK_GREEN, WHITE) and (current_time - last_click_time > CLICK_DELAY):
        current_flashcard = flashcard_weight(biology_notes, current_username)
        show_flashcard_answer = False
        flashcard_xp_awarded = False
        last_click_time = current_time
        return last_click_time, current_flashcard, show_flashcard_answer, flashcard_xp_awarded, xp_popup_text, xp_popup_start_time  
    # Show confidence rating buttons when answer is revealed
    if current_flashcard and show_flashcard_answer:
        last_click_time, flashcard_xp_awarded, xp_popup_text, xp_popup_start_time = confidence_buttons(
            screen, current_time, last_click_time, current_username, flashcard_xp_awarded, 
            current_flashcard, xp_popup_text, xp_popup_start_time
        )
    
    return last_click_time, current_flashcard, show_flashcard_answer, flashcard_xp_awarded, xp_popup_text, xp_popup_start_time 

def confidence_buttons(screen, current_time, last_click_time, current_username,
                      flashcard_xp_awarded, current_flashcard, xp_popup_text, xp_popup_start_time):

    # Create RAG rating buttons
    red_button = pygame.Rect(350, 330, 100, 50)
    amber_button = pygame.Rect(500, 330, 100, 50)
    green_button = pygame.Rect(650, 330, 100, 50)

    # Red button for 2 XP 
    if clickable_button(screen, "Red", red_button, RED, WHITE) and (current_time - last_click_time > CLICK_DELAY):
        set_confidence(current_username, current_flashcard[0], 1)
        if not flashcard_xp_awarded:
            xp_system(current_username, 2)
            xp_popup_text, xp_popup_start_time = xp_popup_animation(2, xp_popup_text, xp_popup_start_time)
            flashcard_xp_awarded = True
            last_click_time = current_time

    # Amber button for 5 XP
    if clickable_button(screen, "Amber", amber_button, AMBER, WHITE) and (current_time - last_click_time > CLICK_DELAY):
        set_confidence(current_username, current_flashcard[0], 2)
        if not flashcard_xp_awarded:
            xp_system(current_username, 5)
            xp_popup_text, xp_popup_start_time = xp_popup_animation(5, xp_popup_text, xp_popup_start_time)
            flashcard_xp_awarded = True
            last_click_time = current_time

    # Green button for 10 XP
    if clickable_button(screen, "Green", green_button, LIGHT_GREEN, WHITE) and (current_time - last_click_time > CLICK_DELAY):
        set_confidence(current_username, current_flashcard[0], 3)
        if not flashcard_xp_awarded:
            xp_system(current_username, 10)
            xp_popup_text, xp_popup_start_time = xp_popup_animation(10, xp_popup_text, xp_popup_start_time)
            flashcard_xp_awarded = True
            last_click_time = current_time
    
    return last_click_time, flashcard_xp_awarded, xp_popup_text, xp_popup_start_time 

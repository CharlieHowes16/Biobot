from ui.config import *
from ui.layout import main_pages_layout
from logic.flashcard_logic import RAG_scores

def performance_page(game_state, screen):

    # Draw page layout and title
    main_pages_layout(game_state, screen)
    text_line(screen, "PERFORMANCE", FONT, BLACK, 500, 10)

    # Get confidence scores
    red, amber, green = RAG_scores()

    # Display RAG breakdown visually
    text_line(screen, f"Red: {red}", SMALL_FONT, RED, 300, 200)
    text_line(screen, f"Amber: {amber}", SMALL_FONT, (255, 191, 0), 300, 250)
    text_line(screen, f"Green: {green}", SMALL_FONT, DARK_GREEN, 300, 300)

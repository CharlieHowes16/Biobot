import pygame
import sqlite3
import random
from ui.config import *
from ui.layout import main_pages_layout
from logic.flashcard_logic import RAG_scores
from logic.xp_system import level_up_system

# Level titles for when a user levels up 
level_titles = {
    1: "Beginner Biologist",
    2: "Cell Explorer",
    3: "Molecule Master",
    4: "DNA Decoder",
    5: "Organism Observer",
    6: "Lab Specialist",
    7: "Bio Analyst",
}

def user_title(level):
    if level in level_titles:
        return level_titles[level]
    return level_titles[level_titles.keys()]

# Colours for the badges 
badge_colours = [
    (1, (205, 127, 50)),     # Bronze
    (2, (192, 192, 192)),    # Silver
    (3, (255, 215, 0)),      # Gold
    (4, (0, 191, 255)),      # Blue
    (5, (138, 43, 226)),     # Purple
    (6, (50, 205, 50)),      # Green
    (7, (255, 105, 180)),    # Pink
]

# Function for drawing badges 
def draw_all_badges(screen, level):
    x = 700   # Starting x position for badges 
    y = 700   # Starting y position for badges 

    text_line(screen, "BADGES :", SMALL_FONT, BLACK, 520, 685)

    for badge_level, colour in badge_colours:
        if badge_level > level:
            break

        pygame.draw.circle(screen, colour, (x, y), 30) # Draws main part of the badge 
        pygame.draw.circle(screen, BLACK, (x, y), 30, 3) # Draws border of the badge 

        
        badge_number = SMALL_FONT.render(str(badge_level), True, BLACK)
        number_area = badge_number.get_rect(center=(x, y))
        screen.blit(badge_number, number_area)

        x = x + 70  # Move next badge to the right



def performance_page(game_state, screen, current_username, biology_notes, current_streak, current_quote=""):

    # Draws page layout and title
    main_pages_layout(game_state, screen, current_username)
    text_line(screen, "PERFORMANCE", FONT, BLACK, 500, 10)

    # Get confidence scores for all flashcards
    red, amber, green, new = RAG_scores(current_username, len(biology_notes))

    # Displays RAG breakdown including cards that havent been studied yet 
    text_line(screen, "Card Breakdown:", FONT, BLACK, 300, 200)
    text_line(screen, f"Red: {red}", SMALL_FONT, RED, 300, 250)
    text_line(screen, f"Amber: {amber}", SMALL_FONT, (255, 191, 0), 300, 300)
    text_line(screen, f"Green: {green}", SMALL_FONT, DARK_GREEN, 300, 350)
    text_line(screen, f"New: {new}", SMALL_FONT, GREY, 300, 400)

    motivational_quotes = [
        "Keep going! You're doing great!",
        "Every card you review makes you smarter!",
        "Biology mastery, one term at a time!",
        "Your brain is growing stronger!",
        "Consistency is the key to success!",
        "You're building knowledge that lasts!",
        "Small steps lead to big achievements!",
        "Your hard work will pay off!",
        "Learning is a superpower!",
        "You're getting better every day!",
        "Knowledge is your greatest asset!",
    ]

    if not current_quote:
        current_quote = random.choice(motivational_quotes)

    text_line(screen, current_quote, SMALL_FONT, DARK_GREEN, 300, 500)

    # Displays the users current streak 
    text_line(screen, f"Streak: {current_streak} days", SMALL_FONT, BLACK, 900, 100)

    # Get users level from user details database
    level_connection = sqlite3.connect("user_details_database.db")
    level_cursor = level_connection.cursor()
    level_cursor.execute("SELECT XP FROM user_details WHERE Username = ?", (current_username,))
    xp = level_cursor.fetchone()[0]
    level_connection.close()

    level = level_up_system(xp)
    title = user_title(level)

    # Show current user motivational title 
    text_line(screen, f"Title: {title}", SMALL_FONT, BLACK, 900, 150)

    # Draw all badges that level has been reached 
    draw_all_badges(screen, level)

    return current_quote

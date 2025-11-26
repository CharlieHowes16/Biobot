import random

# Flashcard and confidence tracking
current_flashcard = None
show_flashcard_answer = False
user_flashcard_confidence = {}
flashcard_xp_awarded = False  # Tracks if XP was already given for current flashcard
current_username = ""

def set_confidence(term, RAG):
    user_flashcard_confidence[term] = RAG

def RAG_scores():
    red = amber = green = 0
    for level in user_flashcard_confidence.values():
        if level == 1:
            red += 1
        elif level == 2:
            amber += 1
        elif level == 3:
            green += 1
    return red, amber, green

def get_random_flashcard(biology_notes):
    global current_flashcard, show_flashcard_answer, flashcard_xp_awarded
    current_flashcard = random.choice(biology_notes)
    show_flashcard_answer = False
    flashcard_xp_awarded = False
    return current_flashcard

def toggle_flashcard_answer():
    global show_flashcard_answer
    show_flashcard_answer = not show_flashcard_answer

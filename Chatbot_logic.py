import pygame
import difflib

# Chatbot variables
chatbot_greeting_displayed = False
chatbot_message = ""
chatbot_message_box = pygame.Rect(270, 110, 860, 60)
chatbot_user_typing_box = pygame.Rect(260, 700, 600, 50)
chatbot_user_typing_text = ""

# Retreives the definition for the term the user asks for 
def biology_term_definition(collect_biology_term):
    clear_terms = blacklist_fillers(collect_biology_term)  
    terms = [term.lower() for term, _ in biology_notes]

    # Try exact match first
    for term, definition in biology_notes:
        if term.lower() == clear_terms:
            return definition
    
    # If no exact match, find closest match using difflib
    closest_matches = difflib.get_close_matches(clear_terms, terms, n=1, cutoff=0.6)
    if closest_matches:
        # Get index of closest match
        closest_term = closest_matches[0]
        for term, definition in biology_notes:
            if term.lower() == closest_term:
                return f"{definition}"
            
    
    return "Sorry, I couldn't find that term."

def xp_popup_animation(amount):
    global xp_popup_text, xp_popup_start_time
    xp_popup_text = f"+{amount} XP"
    xp_popup_start_time = pygame.time.get_ticks()

# Removes any common words like the so sorting questions is more managable
def blacklist_fillers(user_input):
    filler_words = {"what", "is", "the", "a", "an", "define", "meaning", "of", "please"}
    words_entered = user_input.lower().split()
    filtered_words = [word for word in words_entered if word not in filler_words]
    return "".join(filtered_words)

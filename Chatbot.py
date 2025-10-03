# Chatbot variables
chatbot_greeting_displayed = False
chatbot_message = ""
chatbot_message_box = pygame.Rect(270, 110, 860, 60)
chatbot_user_typing_box = pygame.Rect(260, 700, 600, 50)
chatbot_user_typing_text = ""

def blacklist_fillers(user_input):
    filler_words = {"what", "is", "the", "a", "an", "define", "meaning", "of", "please"} # Words to be excluded from the search
    words_entered = user_input.lower().split()
    filtered_words = [word for word in words_entered if word not in filler_words]
    return "".join(filtered_words)

# Retreives the definition for the term the user asks for 
def biology_term_definition(collect_biology_term):
    clear_terms = blacklist_fillers(collect_biology_term) # Removes all of the blacklisted words from the user question
    terms = [term.lower() for term, _ in biology_notes]

    # Try exact match first
    for term, definition in biology_notes:
        if term.lower() == clear_terms:
            return definition
    
    # If no exact match, find closest match using difflib
    closest_matches = difflib.get_close_matches(clear_terms, terms, n=1, cutoff=0.6) # If the entered phrase is more than 60% correct it will return that definition
    if closest_matches:
        # Get index of closest match
        closest_term = closest_matches[0]
        for term, definition in biology_notes:
            if term.lower() == closest_term:
                return f"{definition}"
            
    
    elif game_state == "Chatbot_Page":
        main_pages_layout()
        text_line("CHATBOT", FONT, BLACK, 500, 10)
        pygame.draw.rect(screen, WHITE, chatbot_user_typing_box, 0)  # Filled white box
        pygame.draw.rect(screen, BLACK, chatbot_user_typing_box, 2)  # Black border

        if chatbot_user_typing_text == "" and typing != "chatbot_input":
            chatbot_placeholder_text = SMALL_FONT.render("Ask anything...", True, GREY)
            screen.blit(chatbot_placeholder_text, (chatbot_user_typing_box.x + 10, chatbot_user_typing_box.y + 10))
        else:
            input_text_surface = SMALL_FONT.render(chatbot_user_typing_text, True, BLACK)
            screen.blit(input_text_surface, (chatbot_user_typing_box.x + 10, chatbot_user_typing_box.y + 10))

        pygame.draw.rect(screen, WHITE, chatbot_message_box)
        pygame.draw.rect(screen, BLACK, chatbot_message_box, 2)
        text_line(chatbot_message, SMALL_FONT, BLACK, 280, 120)

import pygame
from ui.config import *
from ui.layout import main_pages_layout

# Function to draw when user is on the chatbot page 
def chatbot_page(screen, typing, chatbot_user_typing_box, chatbot_message_box, game_state, chatbot_user_typing_text, chatbot_message):

    main_pages_layout(game_state, screen)
    text_line(screen, "CHATBOT", FONT, BLACK, 500, 10)
    pygame.draw.rect(screen, WHITE, chatbot_user_typing_box, 0)  # Fills box in white 
    pygame.draw.rect(screen, BLACK, chatbot_user_typing_box, 2)  # Creates a black border

    if chatbot_user_typing_text == "" and typing != "chatbot_input":
        chatbot_placeholder_text = SMALL_FONT.render("Ask anything...", True, GREY) # Placeholder text if nothing has been written yet 
        screen.blit(chatbot_placeholder_text, (chatbot_user_typing_box.x + 10, chatbot_user_typing_box.y + 10))
    else:
        input_text_surface = SMALL_FONT.render(chatbot_user_typing_text, True, BLACK) # Shows the users question when they start typing
        screen.blit(input_text_surface, (chatbot_user_typing_box.x + 10, chatbot_user_typing_box.y + 10))
    
        # Draw chatbot message box
    chatbot_message_box = pygame.Rect(270, 110, 860, 60)
    pygame.draw.rect(screen, WHITE, chatbot_message_box) # Fills box in white 
    pygame.draw.rect(screen, BLACK, chatbot_message_box, 2) # Creates a black border
    
    # Draw chatbot message text
    if chatbot_message:
        wrapped_message = text_wrapping(chatbot_message, 60)  # 60 is the maximum amount of characters before the line is dropped
        start_height = 120 # Starting height of the first line in the chatbot reply 
        line_height = SMALL_FONT.get_height() # Height of one line of small font text 
        
        for line in wrapped_message.split('\n'):
            wrapped_small_font = SMALL_FONT.render(line, True, BLACK)
            screen.blit(wrapped_small_font, (280, start_height))
            start_height += line_height

    return chatbot_user_typing_box

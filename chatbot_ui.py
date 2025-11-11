import pygame
from ui.config import *
from ui.layout import main_pages_layout

def chatbot_page(screen, chatbot_user_typing_box, chatbot_user_typing_text,
                 typing, chatbot_placeholder_text, input_text_surface, chatbot_message_box,
                 chatbot_message)


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

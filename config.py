import pygame

# Colours for all pages
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GREEN = (183, 215, 168)
GREEN = (147, 196, 125)
DARK_GREEN = (116, 167, 99)
RED = (255, 0, 0)
GREY = (128, 128, 128)

pygame.font.init()

# Fonts for all pages
FONT = pygame.font.SysFont("arialblack", 40)
SMALL_FONT = pygame.font.SysFont("arial", 30)
BOLD_FONT = pygame.font.SysFont("arial", 30, bold = True)
ERROR_FONT = pygame.font.SysFont("arial", 15, bold = True)

# Button click timing which prevents rapid clicking
last_click_time = 0
CLICK_DELAY = 300

# Renders and draw text at specific position
def text_line(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y)) 

# Draws a button with a hover effect and checks for clicks
def clickable_button(screen, text, rect, base_color, hover_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if rect.collidepoint(mouse):
        pygame.draw.rect(screen, hover_color, rect) # Highlights button wih a hover colour if mouse is over it
        clicked = click[0] == 1
    else:
        pygame.draw.rect(screen, base_color, rect)
        clicked = False

    # Ensures that writing inside of buttons is centred
    text_surface = SMALL_FONT.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

    return clicked

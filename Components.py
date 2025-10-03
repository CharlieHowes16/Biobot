# Renders and draw text at specific position
def text_line(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y)) 

# Draws a button with a hover effect and checks for clicks
def clickable_button(text, rect, base_color, hover_color):
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

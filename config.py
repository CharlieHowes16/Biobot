# Initialize pygame
pygame.init()

# Biobot screen settings and create window
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("BioBot")

# Colours for all pages
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GREEN = (183, 215, 168)
GREEN = (147, 196, 125)
DARK_GREEN = (116, 167, 99)
RED = (255, 0, 0)
GREY = (128, 128, 128)

# Fonts for all pages
FONT = pygame.font.SysFont("arialblack", 40)
SMALL_FONT = pygame.font.SysFont("arial", 30)
BOLD_FONT = pygame.font.SysFont("arial", 30, bold = True)
ERROR_FONT = pygame.font.SysFont("arial", 15, bold = True)

# Button click timing which prevents rapid clicking
last_click_time = 0
CLICK_DELAY = 300

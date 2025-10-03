# XP variables
xp_popup_text = ""
xp_popup_start_time = 0

# Stores XP user has gained into the user details database
def xp_system(username, points_gained):
    xp_database_connection = sqlite3.connect('user_details_database.db') # Opens the user detail database
    xp_cursor = xp_database_connection.cursor()

    # Retrieves the current XP in the database
    xp_cursor.execute("SELECT XP FROM user_details WHERE Username = ?", (username,))
    xp_result = xp_cursor.fetchone()
    if xp_result:
        current_xp = xp_result[0]
    else:
        current_xp = 0
        # Updates XP if XP is gained
    new_xp = current_xp + points_gained
    xp_cursor.execute("UPDATE user_details SET XP = ? WHERE Username = ?", (new_xp, username))
    xp_database_connection.commit()
    xp_database_connection.close()

# Leveling up system and how much XP is required to level up
def level_up_system(xp):
    level_thresholds = [0, 100, 250, 500, 1000, 5000, 10000] # Each threshold for XP levels

    # Determines user level based on their XP 
    level = 1
    for i in level_thresholds:
        if xp>= i:
            level = level + 1
        else:
            break
    return level - 1

def xp_popup_animation(amount): # When the user completes a flashcard or asks the chatbot a question a xp pop-up appears
    global xp_popup_text, xp_popup_start_time
    xp_popup_text = f"+{amount} XP"
    xp_popup_start_time = pygame.time.get_ticks()

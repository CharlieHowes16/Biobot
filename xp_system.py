import sqlite3

# XP popup animation variables
xp_popup_text = ""
xp_popup_start_time = 0

def xp_system(username, points_gained):
    xp_database_connection = sqlite3.connect('user_details_database.db')
    xp_cursor = xp_database_connection.cursor()

    # Get current XP from database
    xp_cursor.execute("SELECT XP FROM user_details WHERE Username = ?", (username,))
    xp_result = xp_cursor.fetchone()
    current_xp = xp_result[0] if xp_result else 0

    # Update with new XP
    new_xp = current_xp + points_gained
    xp_cursor.execute("UPDATE user_details SET XP = ? WHERE Username = ?", (new_xp, username))
    xp_database_connection.commit()
    xp_database_connection.close()

def level_up_system(xp):
    level_thresholds = [0, 100, 250, 500, 1000, 5000, 10000]  # XP needed for each level
    
    level = 1
    for threshold in level_thresholds:
        if xp >= threshold:
            level += 1
        else:
            break
    return level - 1  # Adjust for initial level

def xp_popup_animation(amount):
    global xp_popup_text, xp_popup_start_time
    xp_popup_text = f"+{amount} XP"
    xp_popup_start_time = pygame.time.get_ticks()

import sqlite3
import pygame

pygame.mixer.init() 
celebration_sound = pygame.mixer.Sound("celebration.mp3") 

def level_up_audio(): 
    celebration_sound.play()

def xp_system(username, points_gained):
    xp_database_connection = sqlite3.connect('user_details_database.db')
    xp_cursor = xp_database_connection.cursor()

    # Get current XP from database
    xp_cursor.execute("SELECT XP FROM user_details WHERE Username = ?", (username,))
    xp_result = xp_cursor.fetchone()
    current_xp = xp_result[0] if xp_result else 0

    # Update with new XP
    new_xp = current_xp + points_gained

    # Level up detection
    old_level = level_up_system(current_xp) 
    new_level = level_up_system(new_xp) 
    if new_level > old_level: 
        level_up_audio()

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

def xp_popup_animation(amount, xp_popup_text, xp_popup_start_time):
    xp_popup_text = f"+{amount} XP"
    xp_popup_start_time = pygame.time.get_ticks()
    
    return xp_popup_text, xp_popup_start_time

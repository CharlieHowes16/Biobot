import sqlite3
import datetime

# Function for changing the users streak
def update_streak(username):
    streak_connection = sqlite3.connect('user_details_database.db') 
    streak_cursor = streak_connection.cursor() 
    
    # Get todays and yesterdays date
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    
    # Get users current streak and their last login date 
    streak_cursor.execute("SELECT LastLogin, Streak FROM user_details WHERE Username = ?", (username,)) 
    result = streak_cursor.fetchone()
    
    if result: 
        last_login_string, current_streak = result 

        # Stops error if users streak is 0 due to new account
        if last_login_string is None:
            new_streak = 1
        else:
            last_login = datetime.datetime.strptime(last_login_string, "%Y-%m-%d").date()

            if last_login == today:  # User has already logged in today so streak does not need to change 
                new_streak = current_streak 
            elif last_login == yesterday: 
                new_streak = current_streak + 1
            else:  
                new_streak = 1
    else:  # New user so they are given their first day streak
        new_streak = 1 
    
    # Update database with new streak and last login 
    streak_cursor.execute( 
        "UPDATE user_details SET LastLogin = ?, Streak = ? WHERE Username = ?", 
        (today.strftime("%Y-%m-%d"), new_streak, username)
    ) 
    streak_connection.commit()
    streak_connection.close() 
    
    return new_streak 

# Funtion to collect the streak from user details database
def get_streak(username): 
    streak_connection = sqlite3.connect('user_details_database.db') 
    streak_cursor = streak_connection.cursor() 
    streak_cursor.execute("SELECT Streak FROM user_details WHERE Username = ?", (username,)) 
    current_streak = streak_cursor.fetchone() 
    streak_connection.close() 
    return current_streak[0] if current_streak else 0

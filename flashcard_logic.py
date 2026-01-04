import random
import sqlite3

# Function to add the users confidence for each biology revision card
def set_confidence(username, term, confidence_level):
    flashcard_confidence_connection = sqlite3.connect('user_details_database.db')
    flashcard_confidence_cursor = flashcard_confidence_connection.cursor()

    flashcard_confidence_cursor.execute('''
        INSERT OR REPLACE INTO flashcard_progress 
        (username, term, confidence)
        VALUES (?, ?, ?)
    ''', (username, term, confidence_level))
    flashcard_confidence_connection.commit()
    flashcard_confidence_connection.close()

# Function to make weaker topics come up more oftehn with a higher weight 
def flashcard_weight(biology_notes, username):
    flashcard_confidence_connection = sqlite3.connect('user_details_database.db')
    flashcard_confidence_cursor = flashcard_confidence_connection.cursor()
    
    # Collect all the confidence levels from the users database
    flashcard_confidence_cursor.execute('SELECT term, confidence FROM flashcard_progress WHERE username = ?', (username,))
    confidence_data = {term: confidence for term, confidence in flashcard_confidence_cursor.fetchall()}
    
    flashcard_confidence_connection.close()

    # Creates 2 lists for the notes that have been weighted and the amount they have been weighted by
    weighted_notes = []
    weights = []

    for term, definition in biology_notes:
        confidence = confidence_data.get(term, 0)  # 0 means that the flashcard has not been seen yet 
        
        if confidence == 1:  # Red confidence level so a high weight to make it come up more often 
            weight = 8
        elif confidence == 2:  # Amber confidence level so a high weight to make it come up slightly less
            weight = 3
        elif confidence == 3:  # Green confidence level so a high weight to make it come up rarely 
            weight = 1
        else:  # Card hasnt yet been seen so it has a medium weight 
            weight = 5
        
        weighted_notes.append((term, definition))
        weights.append(weight)

    # Selects the next card using weighted probabilty based on how confident the user already is 
    if weighted_notes:
        return random.choices(weighted_notes, weights=weights, k=1)[0]
    else:
        return random.choice(biology_notes)

# Function to get the counts of red, amber, green and new cards for the user 
def RAG_scores(username, total_biology_notes_count):
    flashcard_confidence_connection = sqlite3.connect('user_details_database.db')
    flashcard_confidence_cursor = flashcard_confidence_connection.cursor()
    
    flashcard_confidence_cursor.execute('''
        SELECT confidence, COUNT(*) FROM flashcard_progress 
        WHERE username = ? GROUP BY confidence
    ''', (username,))
    
    results = flashcard_confidence_cursor.fetchall()
    flashcard_confidence_connection.close()
    
    # Converts the confidence level from the user into a count 
    counts = {1: 0, 2: 0, 3: 0}
    for confidence, count in results:
        counts[confidence] = count
    
    # Calculate how many cards have not been revised yet 
    total_rated = counts[1] + counts[2] + counts[3]
    new_cards = total_biology_notes_count - total_rated
    
    return counts[1], counts[2], counts[3], new_cards  # Returns red, amber, green, new to be shown on the performance page 

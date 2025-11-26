import difflib
from database.setup_database import setup_database

biology_notes = setup_database()

# Retreives the definition for the term the user asks for 
def biology_term_definition(collect_biology_term):
    clear_terms = blacklist_fillers(collect_biology_term)  
    terms = [term.lower() for term, _ in biology_notes]

    # Try exact match first
    for term, definition in biology_notes:
        if term.lower() == clear_terms:
            return definition
    
    # If no exact match, find closest match using fuzzy search 
    closest_matches = difflib.get_close_matches(clear_terms, terms, n=1, cutoff=0.6) # Words need to be at least 60% correct 
    if closest_matches:
        # Get index of closest match
        closest_term = closest_matches[0]
        for term, definition in biology_notes:
            if term.lower() == closest_term:
                definition = f"{definition}"
                return definition
            
    
    return "Sorry, I couldn't find that term." 

# Removes any common words like the so sorting questions is more managable
def blacklist_fillers(user_input):
    filler_words = {"what", "is", "the", "a", "an", "define", "meaning", "of", "please"} # Words to blacklist 
    words_entered = user_input.lower().split()
    filtered_words = [word for word in words_entered if word not in filler_words]
    return " ".join(filtered_words) # Rejoins the sentance without blacklisted words

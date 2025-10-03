# Connect to the user and biology databases or creates if they don't exist

user_database_connection = sqlite3.connect('user_details_database.db')
user_cursor = user_database_connection.cursor()

biology_database_connection = sqlite3.connect('biology_database.db')
biology_cursor = biology_database_connection.cursor()

# Create new tables if they don't already exist for user details and the biology keywords and definitions
user_cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_details (
        Username TEXT,
        Password BLOB,
        XP INTEGER DEFAULT 0
    )
''')

biology_cursor.execute('''
    CREATE TABLE IF NOT EXISTS biology_notes (
        Terms TEXT,
        Definition TEXT
    )
''')

# Open the CSV file containing biology terms and definitions loading them into the database
with open('biology_terms.csv', 'r') as file: # Allow for special characters
    file_reader = csv.reader(file, delimiter=";")
    next(file_reader)

    for row in file_reader:
        if len(row) != 2:   # Skips any rows missing values or errors
            continue
        biology_cursor.execute(
            "INSERT INTO biology_notes (Terms, Definition) VALUES (?, ?)", row)

    
# Fetch biology key terms so they can be used for the flashcards and chatbot
biology_cursor.execute("SELECT Terms, Definition FROM biology_notes")
biology_notes = biology_cursor.fetchall()


# Close the connection to the databases
user_database_connection.commit()
user_database_connection.close()

biology_database_connection.commit()
biology_database_connection.close()

import sqlite3

def create_database():
    conn = sqlite3.connect('data/users_data.db')
    
    cursor = conn.cursor()
    
    # Users
    cursor.execute('''
    CREATE TABLE "Users" (
        UserID INTEGER PRIMARY KEY,
        TelegramUserID INTEGER UNIQUE,
        UserInfo TEXT,
        UserNick TEXT
    )
    ''')
    
    # Pairs
    cursor.execute('''
    CREATE TABLE "Pairs" (
        PairID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserOne INTEGER,
        UserTwo INTEGER
    )
    ''')
    
    conn.commit()
    conn.close()

create_database()
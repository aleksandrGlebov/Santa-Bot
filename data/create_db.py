import sqlite3

def create_database():
    conn = sqlite3.connect('data/users_data.db')
    
    cursor = conn.cursor()
    
    # Создание таблицы Users
    cursor.execute('''
    CREATE TABLE "Users" (
        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        TelegramUserID INTEGER UNIQUE,
        UserName TEXT,
        UserInfo TEXT,
        UserNick TEXT UNIQUE,
        Role TEXT DEFAULT 'member'
    )
    ''')
    
    # Создание таблицы Pairs
    cursor.execute('''
    CREATE TABLE "Pairs" (
        PairID INTEGER PRIMARY KEY AUTOINCREMENT,
        GiverUserID INTEGER,
        ReceiverUserID INTEGER,
        FOREIGN KEY (GiverUserID) REFERENCES Users(UserID),
        FOREIGN KEY (ReceiverUserID) REFERENCES Users(UserID),
        CHECK (GiverUserID != ReceiverUserID)
    )
    ''')
    
    conn.commit()
    conn.close()

create_database()

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
        Language TEXT,
        RoomID INTEGER,
        FOREIGN KEY (RoomID) REFERENCES Rooms(RoomID)
    )
    ''')
    
    # Создание таблицы Pairs
    cursor.execute('''
    CREATE TABLE "Pairs" (
        PairID INTEGER PRIMARY KEY AUTOINCREMENT,
        GiverUserID INTEGER,
        ReceiverUserID INTEGER,
        RoomID INTEGER,
        FOREIGN KEY (GiverUserID) REFERENCES Users(UserID),
        FOREIGN KEY (ReceiverUserID) REFERENCES Users(UserID),
        FOREIGN KEY (RoomID) REFERENCES Rooms(RoomID),
        CHECK (GiverUserID != ReceiverUserID)
    )
    ''')

    # Создание таблицы Rooms
    cursor.execute('''
    CREATE TABLE "Rooms" (
        RoomID INTEGER PRIMARY KEY AUTOINCREMENT,
        RoomName TEXT,
        AdminUserID INTEGER,
        FOREIGN KEY (AdminUserID) REFERENCES Users(UserID)
    )    
    ''')
    
    conn.commit()
    conn.close()

create_database()

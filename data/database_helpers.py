import sqlite3
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_PATH = "data/users_data.db"

def connect_to_db():
    return sqlite3.connect(DATABASE_PATH)

# Functions for Users table
def create_user(data: dict):
    logger.info("create_user called")

    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO Users (
            TelegramUserID, UserName, UserInfo, UserNick, Language
        ) VALUES (
            :telegramUserID, :userName, :userInfo, :userNick, :language
        )
        """, data)

        conn.commit()

    except sqlite3.Error as e:
        logger.error(f"Error: {e}")

    finally:
        conn.close()

def read_user(telegramUserID):
    logger.info("read_user called")

    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM Users WHERE TelegramUserID = ?', (telegramUserID,))
        user = cursor.fetchone()

        conn.commit()

    except sqlite3.Error as e:
        logger.error(f"Error: {e}")

    finally:
        conn.close()

    return user

def update_user(telegramUserID, parameter, value):
    logger.info("update_user called")

    allowed_parameters = ["UserName", "UserInfo", "UserNick", "Language", "RoomID"]
    if parameter not in allowed_parameters:
        return f"Error: parameter {parameter} is not allowed to be updated."

    try:
        conn = connect_to_db()
        cursor = conn.cursor()
    
        cursor.execute(f'UPDATE Users SET {parameter} = ? WHERE TelegramUserID = ?', (value, telegramUserID))

        conn.commit()

    except sqlite3.Error as e:
        logger.error(f"Error: {e}")

    finally:
        conn.close()

    return f"The {parameter} parameter has been successfully updated"

def delete_user(telegramUserID):
    logger.info("delete_user called")

    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM Users WHERE TelegramUserID = ?', (telegramUserID,))

        if cursor.rowcount == 0:
            conn.close()
            return "User with this ID does not exist in the database"
        else:
            conn.commit()
            return f"User with ID {telegramUserID} has been successfully deleted from the database"
    
    except sqlite3.Error as e:
        logger.error(f"Error: {e}")

    finally:
        conn.close()
    
# Functions for Pairs table
def create_pair(data: dict):
    logger.info("create_pair called")

    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO Pairs (
            GiverUserID, ReceiverUserID, RoomID
        ) VALUES (
            :giverUserID, :receiverUserID, :roomID
        )
        """, data)

        conn.commit()

    except sqlite3.Error as e:
        logger.error(f"Error: {e}")

    finally:
        conn.close()

def read_pair_by_room(roomID):
    logger.info("read_pair_by_room called")

    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM Pairs WHERE RoomID = ?', (roomID,))
        pair = cursor.fetchone()

        conn.commit()

    except sqlite3.Error as e:
        logger.error(f"Error: {e}")

    finally:
        conn.close()

    return pair

def read_pair_by_giverUserID(giverUserID):
    logger.info("read_pair_by_giverUserID called")

    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM Pairs WHERE GiverUserID = ?', (giverUserID,))
        pair = cursor.fetchone()

        conn.commit()

    except sqlite3.Error as e:
        logger.error(f"Error: {e}")

    finally:
        conn.close()

    return pair

def update_pair(pairID, parameter, value):
    logger.info("update_pair called")

    allowed_parameters = ["GiverUserID", "ReceiverUserID"]
    if parameter not in allowed_parameters:
        return f"Error: parameter {parameter} is not allowed to be updated."
    
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        
        cursor.execute(f'UPDATE Pairs SET {parameter} = ? WHERE PairID = ?', (value, pairID))

        conn.commit()

    except sqlite3.Error as e:
        logger.error(f"Error: {e}")

    finally:
        conn.close()

    return f"The {parameter} parameter has been successfully updated"

def delete_pair(pairID):
    logger.info("delete_pair called")

    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM Pairs WHERE PairID = ?', (pairID,))

        if cursor.rowcount == 0:
            conn.close()
            return "The pair with this ID does not exist in the database"
        else:
            conn.commit()
            return f"The pair with ID {pairID} has been successfully deleted from the database"
    
    except sqlite3.Error as e:
        logger.error(f"Error: {e}")

    finally:
        conn.close()
    
# Functions for Rooms table
def create_room(data: dict):
    logger.info("create_room called")

    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO Rooms (
            RoomName, AdminUserID
        ) VALUES (
            :roomName, :adminUserID
        )
        """, data)

        conn.commit()

    except sqlite3.Error as e:
        logger.error(f"Error: {e}")

    finally:
        conn.close()

def read_room(roomID):
    logger.info("read_room called")

    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM Rooms WHERE RoomID = ?', (roomID,))
        room = cursor.fetchone()

        conn.commit()

    except sqlite3.Error as e:
        logger.error(f"Error: {e}")

    finally:
        conn.close()

    return room

def update_room(roomID, parameter, value):
    logger.info("update_room called")

    allowed_parameters = ["RoomName", "AdminUserID"]
    if parameter not in allowed_parameters:
        return f"Error: parameter {parameter} is not allowed to be updated."
    
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        
        cursor.execute(f'UPDATE Rooms SET {parameter} = ? WHERE RoomID = ?', (value, roomID))

        conn.commit()

    except sqlite3.Error as e:
        logger.error(f"Error: {e}")

    finally:
        conn.close()

    return f"The {parameter} parameter has been successfully updated"

def delete_room(roomID):
    logger.info("delete_room called")

    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM Rooms WHERE RoomID = ?', (roomID,))

        if cursor.rowcount == 0:
            conn.close()
            return "The room with this ID does not exist in the database"
        else:
            conn.commit()
            return f"The room with ID {roomID} has been successfully deleted from the database"
    
    except sqlite3.Error as e:
        logger.error(f"Error: {e}")

    finally:
        conn.close()
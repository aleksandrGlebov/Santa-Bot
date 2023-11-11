import sqlite3
import logging

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_PATH = "data/users_data.db"

def connect_to_db():
    return sqlite3.connect(DATABASE_PATH)

# Functions for Users table
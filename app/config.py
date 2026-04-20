import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="shinchan08", # MUST MATCH run.py
        database="music_library"
    )
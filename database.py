# database.py
import sqlite3

DB_NAME = "mothers_day.db"

def connect():
    return sqlite3.connect(DB_NAME)

def create_tribute_table():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tributes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            tribute TEXT,
            image_path TEXT,
            ai_caption TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_tribute(name, tribute, image_path, ai_caption):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tributes (name, tribute, image_path, ai_caption)
        VALUES (?, ?, ?, ?)
    ''', (name, tribute, image_path, ai_caption))
    conn.commit()
    conn.close()

def get_all_tributes():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tributes ORDER BY created_at DESC')
    results = cursor.fetchall()
    conn.close()
    return results

def create_wisdom_table():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wisdom (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            mom_quote TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_wisdom(user_name, mom_quote):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO wisdom (user_name, mom_quote)
        VALUES (?, ?)
    ''', (user_name, mom_quote))
    conn.commit()
    conn.close()

def get_all_wisdom():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM wisdom ORDER BY created_at DESC')
    results = cursor.fetchall()
    conn.close()
    return results

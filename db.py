import sqlite3
from datetime import datetime

DB_NAME = "weather_data.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            temperature REAL NOT NULL,
            windspeed REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def create_connection(db_file=DB_NAME):
    conn = sqlite3.connect(db_file)
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            temperature REAL,
            windspeed REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_weather_data(city, temperature, windspeed):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO weather (city, temperature, windspeed, timestamp) VALUES (?, ?, ?, ?)",
                   (city, temperature, windspeed, timestamp))
    conn.commit()
    conn.close()

def fetch_all_data():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM weather ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def alter_table_add_timestamp():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE weather ADD COLUMN timestamp DATETIME DEFAULT CURRENT_TIMESTAMP")
        conn.commit()
    except sqlite3.OperationalError:
        pass
    conn.close()
def update_record(record_id, new_temp):
    conn = create_connection()
    c = conn.cursor()
    c.execute("UPDATE weather SET temperature = ? WHERE id = ?", (new_temp, record_id))
    conn.commit()
    conn.close()
def delete_record(record_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute("DELETE FROM weather WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()

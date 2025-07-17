import sqlite3

def init_db():
    conn = sqlite3.connect("weather_data.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            temperature REAL,
            windspeed REAL,
            time TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_weather_data(city, temperature, windspeed, time):
    conn = sqlite3.connect("weather_data.db")
    c = conn.cursor()
    c.execute('''
        INSERT INTO weather (city, temperature, windspeed, time)
        VALUES (?, ?, ?, ?)
    ''', (city, temperature, windspeed, time))
    conn.commit()
    conn.close()

def get_all_data():
    conn = sqlite3.connect("weather_data.db")
    c = conn.cursor()
    c.execute("SELECT * FROM weather")
    rows = c.fetchall()
    conn.close()
    return rows

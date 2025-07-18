import sqlite3

def init_db():
    conn = sqlite3.connect("weather_data.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            temperature REAL,
            weather_description TEXT,
            windspeed REAL,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()


def create_connection(db_file="weather_data.db"):
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
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO weather (city, temperature, windspeed)
        VALUES (?, ?, ?)
    ''', (city, temperature, windspeed))
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
        # العمود موجود بالفعل
        pass
    conn.close()

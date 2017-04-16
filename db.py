import sqlite3
from weather_config import get_config

def get_connection():
    config = get_config()
    return sqlite3.connect(config.db_path)


def setup_database(conn):
    with conn as c:
        # Create table
        c.execute('''CREATE TABLE IF NOT EXISTS OAuthDetails 
        (google_plus_id NVARCHAR PRIMARY KEY,
        refresh_token NVARCHAR, 
        access_token NVARCHAR)''')

        c.execute('''CREATE TABLE IF NOT EXISTS WeatherLocation
        (google_plus_id NVARCHAR,
        location_name NVARCHAR,
        FOREIGN KEY (google_plus_id) REFERENCES OAuthDetails(google_plus_id),
        CONSTRAINT WeatherLocation_PK PRIMARY KEY (google_plus_id, location_name)
        )''')

        c.execute('''CREATE TABLE IF NOT EXISTS UpdateJobs 
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        uid NVARCHAR, 
        last_update_time DATETIME, 
        FOREIGN KEY (uid) REFERENCES OAuthDetails(google_plus_id))''')

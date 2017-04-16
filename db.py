import sqlite3

def get_connection():
  return sqlite3.connect('database.db')

def setup_database(conn):
  c = conn.cursor() 
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
    FOREIGN KEY (uid) REFERENCES OAuthDetails(google_plus_id))''');

  conn.commit()
  conn.close()

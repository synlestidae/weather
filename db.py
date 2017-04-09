import sqlite3

def get_connection():
  return sqlite3.connect('database.db')

conn = get_connection()

c = conn.cursor() 
# Create table
c.execute("CREATE TABLE IF NOT EXISTS Users (uid INT IDENTITY PRIMARY KEY, email_address NVARCHAR)")
c.execute('''CREATE TABLE IF NOT EXISTS OAuthDetails 
  (id INT IDENTITY PRIMARY KEY,
  uid INT IDENTITY NOT NULL, 
  refresh_token NVARCHAR, 
  access_token NVARCHAR, 
  access_token_expiry_utc DATETIME,
  FOREIGN KEY (uid) REFERENCES Users(uid))''')
c.execute('''CREATE TABLE IF NOT EXISTS UpdateJobs 
  (id INT IDENTITY PRIMARY KEY,
  uid INT IDENTITY, 
  last_update_time DATETIME, 
  FOREIGN KEY (uid) REFERENCES Users(uid))''');

# Insert a row of data
#/c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()

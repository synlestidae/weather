import sqlite3

def get_connection():
  return sqlite3.connect('database.db')

conn = get_connection()

c = conn.cursor() 
# Create table
c.execute('''CREATE TABLE IF NOT EXISTS OAuthDetails 
  (refresh_token NVARCHAR, 
  access_token NVARCHAR)''')

c.execute('''CREATE TABLE IF NOT EXISTS UpdateJobs 
  (id INT IDENTITY PRIMARY KEY,
  uid INTEGER IDENTITY, 
  last_update_time DATETIME, 
  FOREIGN KEY (uid) REFERENCES OAuthDetails(ROWID))''');

# Insert a row of data
#/c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()

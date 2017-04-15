import db
from oauth2 import random_string
from datetime import datetime

def get_users_obj():
  conn = db.get_connection()
  cursor = conn.get_cursor()
  return Users(cursor)

class Users:
  def __init__(self, cursor):
    self.cursor = cursor

  def register_user(self, user_id, access_token, refresh_token):
    self.cursor.execute('INSERT INTO OAuthDetails VALUES (?, ?, ?)', (user_id, access_token, refresh_token))
    self.cursor.commit()

  def update_credentials(self, user_id, access_token, refresh_token):
    self.cursor.execute('UPDATE OAuthDetails SET access_token=?, refresh_token=?', (user_id, access_token, refresh_token))
    self.cursor.commit()

  def user_exists(self, user_id):
    result = self.cursor.execute("SELECT * FROM OAuthDetails WHERE google_plus_id=?", (user_id))  
    return len(result.fetchone()) > 0

  def get_credentials(self, user_id):
    result = self.cursor.execute("SELECT access_token from OAuthDetails WHERE google_plus_id=?", (user_id))
    row = result.fetchone()
    access_token = row[0]

  def update_job(self, user_id):
    self.cursor.execute('INSERT INTO UpdateJobs VALUES (?, ?, ?)', (user_id, datetime.utcnow()))
    self.cursor.commit()

  def last_update_time(user_id):
    result = self.cursor.execute("SELECT last_update_time FROM UpdateJobs WHERE uid=? ORDER BY last_update_time DESC")
    row_result = result.fetchone()
    if len(row_result) > 0:
      return row_result[0][0]
    return None

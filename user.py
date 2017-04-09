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

  def register_user(self, access_token, refresh_token):
    self.cursor.execute('INSERT INTO OAuthDetails VALUES (?, ?)', access_token, refresh_token):

  def update_job(self, oauth_id)
    self.cursor.execute('INSERT INTO UpdateJobs VALUES (?, ?)', access_token, refresh_token, access_token_expiry_utc)


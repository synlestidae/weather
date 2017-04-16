import db
from oauth2 import random_string
from oauth2client.client import AccessTokenCredentials
from oauth2client import GOOGLE_TOKEN_URI, GOOGLE_REVOKE_URI
from oauth2client import client
from datetime import datetime
import json

def get_users_obj():
  conn = db.get_connection()
  cursor = conn.get_cursor()
  return Users(cursor)

class Users:
  def __init__(self, cursor):
    self.cursor = cursor

  def register_user(self, user_id, access_token, refresh_token):
    print "USER!", user_id, access_token, refresh_token
    self.cursor.execute('INSERT INTO OAuthDetails VALUES (?, ?, ?)', (user_id, access_token, refresh_token))
    #self.cursor.commit()

  def get_users(self):
    result = self.cursor.execute("SELECT google_plus_id FROM OAuthDetails")
    return map(lambda row: row[0], result.fetchall()) 
  def add_location(self, user_id, location_name):
    if location_name not in self.get_locations(user_id):
      self.cursor.execute('INSERT INTO WeatherLocation VALUES (?, ?)', 
        (user_id, location_name))
      #self.cursor.commit()

  def get_locations(self, user_id):
    result = self.cursor.execute("SELECT * FROM WeatherLocation OAuthDetails WHERE google_plus_id=?", (user_id,))
    print dir(result)
    return result.fetchall()

  def update_credentials(self, user_id, access_token, refresh_token):
    self.cursor.execute('UPDATE OAuthDetails SET access_token=?, refresh_token=?', (user_id, access_token, refresh_token))
    #self.cursor.commit()

  def user_exists(self, user_id):
    print "usy", user_id
    result = self.cursor.execute("SELECT * FROM OAuthDetails WHERE google_plus_id=?", (user_id,))  
    if result is not None:
      fetched_row = result.fetchone()
      if fetched_row is not None:
        return len(fetched_row) > 0
    return False

  def get_credentials(self, user_id):
    result = self.cursor.execute("SELECT access_token, refresh_token from OAuthDetails WHERE google_plus_id=?", (user_id,))
    row = result.fetchone()
    access_token = row[0][0]
    refresh_token = row[0][1]
    http = Http()
    credentials = AccessTokenCredentials(access_token, "antunovic-calendar-client/1.0")
    token_info = credentals.get_access_token(http)

    if token_info.expires_in > 60 * 2:
      return credentials 

    with open("client_secrets.json") as client_secrets_file:
      data = json.load(client_secrets_file)  
      token_uri = data["web"]["token_uri"]
      client_id = data["web"]["client_id"]
      client_secret = data["web"]["client_secret"]
      google_token_uri = data["web"]["client_id"]

      return client.OAuth2Credentials(None, client_id, client_secret, 
        refresh_token, None, GOOGLE_TOKEN_URI, None, 
        revoke_uri=GOOGLE_REVOKE_URI)

  def update_job(self, user_id):
    self.cursor.execute('INSERT INTO UpdateJobs VALUES (?, ?, ?)', (user_id, datetime.utcnow()))
    #self.cursor.commit()

  def last_update_time(user_id):
    result = self.cursor.execute("SELECT last_update_time FROM UpdateJobs WHERE uid=? ORDER BY last_update_time DESC")
    row_result = result.fetchone()
    if len(row_result) > 0:
      return row_result[0][0]
    return None

import db

def get_users_obj():
  conn = db.get_connection()
  cursor = conn.get_cursor()
  return Users(cursor)

class Users:
  def __init__(self, cursor):
    self.cursor = cursor

  def register_user(self, email_address):
    self.cursor.execute('INSERT INTO Users VALUES (?)', email_address)

  def get_uid_from_email(self, email_address):
    result = self.cursor.execute('SELECT uid FROM Users where email_address=?', email_address).fetchone()
    return result[0]

  def set_access_token(self, uid, access_token):
    self.cursor.execute("UPDATE Users SET access_token=? WHERE uid=? LIMIT 1", uid, access_token)

  def set_refresh_token(self, uid, refresh_token):
    self.cursor.execute("UPDATE Users SET refresh_token=? WHERE uid=? LIMIT 1", uid, access_token)

  def get_access_token(self, uid):
    result = self.cursor.execute('SELECT access_token FROM Users where uid=?', uid).fetchone()
    return result[0]

  def get_refresh_token(self, uid):
    result = self.cursor.execute('SELECT refresh_token FROM Users where uid=?', uid).fetchone()
    return result[0]

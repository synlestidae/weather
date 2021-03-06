#!/usr/bin/env python

import db
from oauth2 import random_string
from oauth2client.client import AccessTokenCredentials
from oauth2client import GOOGLE_TOKEN_URI, GOOGLE_REVOKE_URI
from oauth2client import client
from datetime import datetime
import dateutil.parser
print dir(dateutil.parser)
from httplib2 import Http
import json


def get_users_obj():
    conn = db.get_connection()
    return Users(conn)


class Users:
    def __init__(self, conn):
        self.conn = conn

    def register_user(self, user_id, access_token, refresh_token):
        print "refresh tht shiw", refresh_token
        with self.conn:
            self.conn.execute('INSERT INTO OAuthDetails VALUES (?, ?, ?)',
                              (user_id, access_token, refresh_token))

    def get_users(self):
        with self.conn:
            result = self.conn.execute(
                "SELECT google_plus_id FROM OAuthDetails")
            rows = result.fetchall()
            return map(lambda row: row[0], rows)

    def add_location(self, user_id, location_name):
        with self.conn:
            locations = self.get_locations(user_id)
            if location_name not in locations:
                self.conn.execute('INSERT INTO WeatherLocation VALUES (?, ?)',
                                  (user_id, location_name))

    def get_locations(self, user_id):
        with self.conn:
            result = self.conn.execute(
                "SELECT * FROM WeatherLocation OAuthDetails WHERE google_plus_id=?", (user_id,))
            return map(lambda row: row[1], result.fetchall())

    def update_credentials(self, user_id, access_token, refresh_token):
        with self.conn:
            self.conn.execute('UPDATE OAuthDetails SET access_token=?, refresh_token=? WHERE google_plus_id=?',
                              (access_token, refresh_token, user_id, ))

    def user_exists(self, user_id):
        with self.conn:
            result = self.conn.execute(
                "SELECT * FROM OAuthDetails WHERE google_plus_id=?", (user_id,))
            if result is not None:
                fetched_row = result.fetchone()
                if fetched_row is not None:
                    return len(fetched_row) > 0
            return False

    def get_credentials(self, user_id):
        with self.conn:
            result = self.conn.execute(
                "SELECT access_token, refresh_token from OAuthDetails WHERE google_plus_id=?", (user_id,))
            row = result.fetchone()
            access_token = row[0]
            refresh_token = row[1]
            print "tokens", refresh_token
            http = Http()
            credentials = AccessTokenCredentials(access_token, "antunovic-calendar-client/1.0")
            token_info = credentials.get_access_token(http)

            print "Still okay? ", token_info.expires_in
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
        with self.conn:
            self.conn.execute(
                'INSERT INTO UpdateJobs VALUES (?, ?, ?)', (None, user_id, datetime.utcnow()))

    def last_update_time(self, user_id):
        with self.conn:
            result = self.conn.execute(
                "SELECT last_update_time FROM UpdateJobs WHERE uid=? ORDER BY last_update_time DESC", (user_id,))
            row_result = result.fetchone()
            if row_result is not None and len(row_result) > 0:
                last_update_time = row_result[0]
                return dateutil.parser.parse(last_update_time)
            return None

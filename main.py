from flask import Flask, render_template, request
from oauth2 import get_flow 
import httplib2
from datetime import datetime
from apiclient import discovery
from user import Users
from db import get_connection, setup_database
from weather import WeatherReport
from google_calendar import GoogleCalendar
from httplib2 import Http

app = Flask(__name__)

scopes = ["https://www.googleapis.com/auth/calendar"]

@app.route("/")
def root():
  flow = get_flow()
  auth_uri = flow.step1_get_authorize_url()
  return render_template("index.html", oauth_url=auth_uri)

@app.route("/oauth/google")
def authorise_new_user():
  person_id = app.authorise_user(code, state)
  ensure_calendar_updated(person_id) 
  return render_template("done.html")

if __name__ == "__main__":
  app.run(debug=True)

conn = get_connection()
setup_database(conn)

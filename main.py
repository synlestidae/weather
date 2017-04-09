from flask import Flask, render_template, request
from oauth2 import get_flow 
import httplib2
from datetime import datetime
from apiclient import discovery
from user import Users
from db import get_connection
from weather import WeatherReport
from google_calendar import GoogleCalendar

app = Flask(__name__)

scopes = ["https://www.googleapis.com/auth/calendar"]

@app.route("/")
def root():
  flow = get_flow()
  auth_uri = flow.step1_get_authorize_url()
  #return app.send_static_file("index.html", {"oauth_url": auth_uri})
  return render_template("index.html", oauth_url=auth_uri)

@app.route("/oauth/google")
def authorise_new_user():
  #Do the OAuth
  flow = get_flow()
  code = request.args.get('code')
  state = request.args.get('state')
  credentials = flow.step2_exchange(code)
  access_token = credentials.get_access_token()
  refresh_token = credentials.refresh_token

  #Connect to DB
  conn = get_connection()
  cursor = conn.cursor()

  users = Users(cursor)
  report = WeatherReport('wellington')
  print("THe stuff", str(access_token), str(refresh_token), type(access_token), type(refresh_token))
  print(dir(refresh_token))
  print(dir(access_token))
  #users.register_user(access_token, refresh_token)
  google_calendar = GoogleCalendar(credentials, httplib2.Http())
  date_now = datetime.utcnow()
  google_calendar.set_daily_report(date_now, report.brief_summary(), 
    report.full_summary())

  return render_template("done.html", oauth_url=auth_uri)


if __name__ == "__main__":
  app.run()

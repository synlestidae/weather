from flask import Flask, render_template, request
from oauth2 import get_flow 
import httplib2
from datetime import datetime
from apiclient import discovery
from user import Users
from db import get_connection
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
  #Get access and refresh tokens
  flow = get_flow()
  code = request.args.get('code')
  state = request.args.get('state')
  credentials = flow.step2_exchange(code)
  access_token = credentials.get_access_token()
  refresh_token = credentials.refresh_token

  #init http object used by requests
  http = Http()
  credentials.authorize(http)

  #Identify this person
  people_resource = discovery.build("plus", "v1", http=http)
  people_document = people_resource.people().get(userId="me").execute()
  person_id = people_document["id"]

  #Connect to DB - used for managing users
  conn = get_connection()
  cursor = conn.cursor()

  #Register the user or update credentials
  users = Users(cursor)
  users.register_user(person_id, access_token, refresh_token)

  if users.user_exists(person_id):
    user.update_credentials(person_id, access_token, refresh_token)
  else:
    user.register_user(person_id, access_token, refresh_token)

  #now actually post the weather report
  report = WeatherReport('wellington')
  google_calendar = GoogleCalendar(credentials, httplib2.Http())

  users.update_job(person_id)

  for day_report in report.get_days():
    google_calendar.set_daily_report(day_report.date, day_report.brief_summary, day_report.full_summary)

  return render_template("done.html")

if __name__ == "__main__":
  app.run(debug=True)

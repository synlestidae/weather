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

def ensure_calendar_updated(person_id, conn, http=Http()):
  users = Users(conn)

  last_update_time = users.last_update_time(person_id)

  if last_update_time and (last_update_time - datetime.utcnow()).total_seconds() < 60 * 60 * 4:
    return update_calendar_one_user(person_id, users, http)

def update_calendar_one_user(person_id, users, http):
  #Register the user or update credentials
  locations = users.get_locations(person_id)

  if len(locations) < 1:
    return

  location = locations[0]

  #now actually post the weather report
  report = WeatherReport(location)
  credentials = users.get_credentials()
  google_calendar = GoogleCalendar(credentials, http)

  for day_report in report.get_days():
    google_calendar.set_daily_report(day_report.date, 
      day_report.brief_summary, 
      day_report.full_summary)

  users.update_job(person_id)

  return render_template("done.html")

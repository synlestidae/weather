from flask import Flask, render_template, request
from oauth2 import get_flow
import httplib2
from datetime import datetime
from apiclient import discovery
from user import Users
from db import get_connection, setup_database
from weather import WeatherReport
from google_calendar import GoogleCalendar
from update import ensure_calendar_updated
from httplib2 import Http
from app import authorise_user
from weather_config import get_config

app = Flask(__name__)

scopes = ["https://www.googleapis.com/auth/calendar"]


@app.route("/")
def root():
    flow = get_flow()
    auth_uri = flow.step1_get_authorize_url()
    return render_template("index.html", oauth_url=auth_uri)


@app.route("/oauth/google")
def authorise_new_user():
    code = request.args.get("code")
    state = request.args.get("state")
    conn = get_connection()
    users = Users(conn)
    person_id = authorise_user(code, state, conn=conn)
    users.add_location(person_id, "wellington")
    ensure_calendar_updated(person_id, conn)
    return render_template("done.html")


if __name__ == "__main__":
    config = get_config()
    app.run(debug=config.debug)

conn = get_connection()
setup_database(conn)
del conn

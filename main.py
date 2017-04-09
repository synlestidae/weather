from flask import Flask, render_template, request
from oauth2 import get_flow 
import httplib2
from apiclient import discovery
from user import Users
from db import get_connection

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
  flow, state = get_flow()
  code = request.args.get('code')
  state = request.args.get('state')
  credentials = flow.step2_exchange(code)
  access_token = credentials.get_access_token()
  refresh_token = credentials.refresh_token

  #Connect to DB
  conn = get_connection()
  cursor = conn.cursor()

  #Identify the user
  #credentials = get_credentials()
  #http = credentials.authorize(httplib2.Http())
  #service = discovery.build('people', 'v1', http=http,
  #  discoveryServiceUrl='https://people.googleapis.com/$discovery/rest') 
  #people_service = service.people()
  #print(dir(service))
  #print(dir(people_service))
  
  user = Users(cursor)
  raise "Not yet implemented"

if __name__ == "__main__":
  app.run()

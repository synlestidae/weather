from oauth2 import get_flow 
import httplib2
from datetime import datetime
from apiclient import discovery
from user import Users
from db import get_connection
from weather import WeatherReport
from google_calendar import GoogleCalendar
from httplib2 import Http

def authorise_user(code, state, http=Http(), conn=get_connection()):
  flow = get_flow()
  credentials = flow.step2_exchange(code, http=http)
  access_token = credentials.get_access_token().access_token
  refresh_token = credentials.refresh_token

  credentials.authorize(http)

  people_resource = discovery.build("plus", "v1", http=http)
  people_document = people_resource.people().get(userId="me").execute()
  person_id = people_document["id"]

  users = Users(conn)

  if users.user_exists(person_id):
    users.update_credentials(person_id, access_token, refresh_token)
  else:
    users.register_user(person_id, access_token, refresh_token)

  return person_id

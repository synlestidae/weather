#from apiclient.discovery import build
from apiclient import discovery
from datetime import datetime

VERSION_FIELD = "weatherCalAntunovic"
CURRENT_VERSION = "0.0.1"

class GoogleCalendar:
  def __init__(self, credentials, http):
    self.http = credentials.authorize(http)
    self.service = discovery.build("calendar", "v3", http=http)

  def clear_event(self, date_when):
    pass

  def set_daily_report(self, date_when, title, description):
    now = datetime.utcnow()
    service = self.service
    date_str = date_when.strftime('%Y-%m-%d')
    body = {
      "summary": title,
      "description": description,
      "start": {
        "date": date_str
      },
      "end": {
        "date": date_str

      },
      "extendedProperties": {
        "private": {
          VERSION_FIELD: CURRENT_VERSION
        }
      }
    }

    #First clear out any old events
    result = service.events().list(calendarId='primary', 
      timeMin=date_when.isoformat(),
      singleEvents=True,
      orderBy='startTime',
      maxResults=10,
      privateExtendedProperty="%s=%s" % (VERSION_FIELD, CURRENT_VERSION)).execute()

    if isinstance(result, dict) and "items" in result:
      events = result["items"]
      for event in events:
        if okay_to_delete(event, now):
          iCalUID = event["iCalUID"]
          service.events().delete(calendarId='primary', eventId=iCalUID) 

def okay_to_delete(event, now):
  now = now.date()
  date_string = event["start"]["date"][0:10]
  date = datetime.strptime(date_string, "%Y-%m-%d").date()
  if (date < now):
    return False
  props = event["extendedProperties"]
  if "private" in props and VERSION_FIELD in props["private"]:
    return True

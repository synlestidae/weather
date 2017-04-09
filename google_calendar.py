#from apiclient.discovery import build
from apiclient import discovery

class GoogleCalendar:
  def __init__(self, credentials, http):
    self.http = credentials.authorize(http)
    self.service = discovery.build("calendar", "v3", http=http)

  def clear_event(self, date_when):
    pass

  def set_daily_report(self, date_when, title, description):
    service = self.service
    date_str = date_when.strftime('%Y-%M-%d')
    body = {
      "summary": title,
      "description": description,
      "start": {
        "date": date_str
      },
      "end": {
        "date": date_str

      }
    }
    service.events().insert(calendarId='primary', body=body).execute()

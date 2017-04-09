from apiclient.discovery import build
service = build("api_name", "api_version")

class GoogleCalendar:
  def __init__(self, credentials, http):
    self.http = credentials.authorize(http)
    self.service = discovery.build("calendar", "v3", http=http)

  def clear_event(self, date_when):
    pass

  def set_daily_report(self, date_when, title, description):
    calendar_meta = service.calendars().get("primary")
    calendar_id = calendar_meta["id"]
    body = {
      "summary": title,
      "description": description,
      "start": {
        "date": date_when.strftime('%Y-%M-%d')
      },
      "end": {
        "date": date_when.strftime('%Y-%M-%d')

      }
    }
    service.events().insert(calendar_id, body)

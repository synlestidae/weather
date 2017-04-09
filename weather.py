sys.path.insert(0, './metservice-api-py/')

import metservice

class WeatherReport:
  def __init__(self, city):
    url = ''.join(metservice.METSERVICE_BASE. API_OPTIONS[forecast_kind].format(city))
    self.report = metservice.get_response(url)

  def morning_temp(self):
    return (0, 0)

  def midday_temp(self):
    return (0, 0)

  def evening_temp(self):
    return (0, 0);

  def brief_summary(self):
    return "Rain, followed by rain"

  def full_summary(self):
    return self.brief_summary()

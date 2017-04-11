import sys

sys.path.insert(0, './metservice-api-py/')

import metservice

class WeatherReport:
  def __init__(self, city):
    forecast_kind = 'LOCAL_FORECAST'
    url = ''.join([metservice.METSERVICE_BASE, metservice.API_OPTIONS[forecast_kind].format(city)])
    self.report = metservice.get_response(url)

  def get_days(self):
    pass

class DayReport:
  def __init__(self, day_report):
    self.day_report = day_report;

  def brief_summary(self):
    return self.day_report["forecast"]

  def full_summary(self):
    high_temp= self.day_report["max"]
    min_temp = self.day_report["min"]
    temp_forecast = "High of %sC and low of %sC." % (high_temp, low_temp)
    full_day_report = "%s. %s" % (temp_forcast, self.brief_summary())

    for period in ["morning", "afternoon", "evening", "overnight"]:
      full_day_report = "%s\n%s: %s." % (full_day_report, period, self.day_report["partDayData"][period])

    return full_day_report

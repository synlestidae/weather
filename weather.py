import sys
import dateutil.parser
import json

sys.path.insert(0, './metservice-api-py/')

import metservice

class WeatherReport:
  def __init__(self, city):
    forecast_kind = 'LOCAL_FORECAST'
    url = ''.join([metservice.METSERVICE_BASE, metservice.API_OPTIONS[forecast_kind], city])
    self.report = metservice.get_response(url)
    self.days = self.get_days()

  def get_days(self):
    days = []
    for (i, day_report) in enumerate(self.report["days"]):
      days.append(DayReport(day_report))
    return days

class DayReport:
  def __init__(self, day_report):
    self.day_report = day_report
    self.date = dateutil.parser.parse(day_report["dateISO"])
    self.__init()
 
  def __init(self):
    self.brief_summary = self.make_brief_summary()
    self.full_summary = self.make_full_summary()

  def make_brief_summary(self):
    return self.day_report["forecast"]

  def make_full_summary(self):
    high_temp= self.day_report["max"]
    min_temp = self.day_report["min"]
    temp_forecast = "High of %sC and low of %sC" % (high_temp, min_temp)
    full_day_report = "%s. %s" % (temp_forecast, self.brief_summary)
    if ("partDayData" in self.day_report):
      report = self.day_report["partDayData"]
      for period in ["morning", "afternoon", "evening", "overnight"]:
        full_day_report = "%s\n%s: %s." % (full_day_report, period, report[period])

    return full_day_report

if __name__ == "__main__":
  w = WeatherReport("wellington")
  for d in w.get_days():
    print d.date
    print d.full_summary

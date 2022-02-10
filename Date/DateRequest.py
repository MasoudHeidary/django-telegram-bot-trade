from persiantools.jdatetime import JalaliDateTime, timedelta
import datetime


def valid_days(max_day):
    today = JalaliDateTime.today() + timedelta(hours=2)
    days = []
    for i in range(1, max_day + 1):
        days += [(today + datetime.timedelta(days=i)).strftime("%Y/%m/%d")]
    return days

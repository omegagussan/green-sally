#!/usr/bin/python3

from datetime import datetime

end_hour = 17
start_hour = 9

def is_weekday(dt):
    return dt.weekday() < 5


def is_working_hours(dt):
    return start_hour < dt.hour < end_hour


def is_working_time():
    now = datetime.now()
    return is_weekday(now) and is_working_hours(now)


def time_until_end_of_day():
    now = datetime.now()
    end_of_day = datetime(now.year, now.month, now.day, end_hour, 0)
    return (end_of_day - now).total_seconds()


def time_until_next_working_day():
    now = datetime.now()
    if now.isoweekday() in set((5, 6)):
        next_working_day = now.date() + datetime.timedelta(days=now.isoweekday() % 5)
        start_of_day = datetime(next_working_day.year, next_working_day.month, next_working_day.day, start_hour, 0)
    else:
        now_date = now.date()
        start_of_day = datetime(now_date.year, now_date.month, now_date.day + 1, start_hour, 0)
    return (start_of_day - now).total_seconds()

#!/usr/bin/python3

from datetime import datetime


def is_weekday(dt):
    return dt.weekday() < 5


def is_working_hours(dt):
    return 9 < dt.hour < 17


def is_working_time():
    now = datetime.now()
    return is_weekday(now) and is_working_hours(now)

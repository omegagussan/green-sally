#!/usr/bin/python3

import time
import random
from src.working_time import is_working_time, time_until_end_of_day, time_until_next_working_day
from src.adjust_desk import AdjustDesk
from src.state import get_state

adjust_desk = AdjustDesk()
raised_time = (20 * 60)


class StatePositionException(Exception):
    pass


def wait_until_next_operation():
    min = 45  # minutes
    max = 120  # minutes
    delay = random.randint(min, max) * 60
    if time_until_end_of_day() < delay:
        return time_until_end_of_day()
    return delay


def wait_standing():
    return raised_time


while True:
    if is_working_time():
        state = get_state()
        if state["position"] == 1:
            adjust_desk.lower_desk()
            time.sleep(wait_until_next_operation())
        elif state["position"] == 0:
            adjust_desk.raise_desk()
            time.sleep(wait_standing())
        else:
            raise StatePositionException("Unknown position")
    else:
        # return to lower state unless in lower-state
        if state["position"] != 0:
            adjust_desk.lower_desk()
        time.sleep(time_until_next_working_day())

#!/usr/bin/python3

import time
import random
from src.working_time import is_working_time, time_until_end_of_day, time_until_next_working_day
from src.adjust_desk import AdjustDesk
from src.state import State
from src.height_sensor import HeightSensor
import os

adjust_desk = AdjustDesk()
state = State()
height_sensor = HeightSensor()
state.set_state_value("position", height_sensor.get())
raised_time = int(os.environ['RAISED_TIME']) if os.environ['RAISED_TIME'] else (20 * 60)
disable_working_hours = True if os.environ['DISABLE_WORKING_TIME'] else False

resolution_time = 1


class StatePositionException(Exception):
    pass


def wait_until_next_operation():
    min = 45  # minutes
    max = 120  # minutes
    delay = random.randint(min, max) * 60
    if time_until_end_of_day() < delay and not disable_working_hours:
        return time_until_end_of_day()
    return delay


def wait_standing():
    return raised_time


def next_action_to_epoch_s(next_s):
    return round(int(time.time()) + next_s)


def update_state(state, wait_time):
    state.set_state_value("next_action", next_action_to_epoch_s(wait_time))
    state.set_state_value("last_action", int(round(time.time())))


while True:
    if is_working_time() or disable_working_hours:
        now_ts = int(round(time.time()))
        state.set_state_value("position", height_sensor.get())
        if state.state["next_action"] > now_ts:
            time.sleep(resolution_time)
        else:
            if state.state["position"] > adjust_desk.threshold():
                adjust_desk.lower_desk(state)
                update_state(state, wait_until_next_operation())
            elif state.state["position"] <= adjust_desk.threshold():
                adjust_desk.raise_desk(state)
                update_state(state, wait_standing())
            else:
                raise StatePositionException("Unknown position")
    else:
        # return to lower state unless in lower-state
        time.sleep(10)
        if state.state["position"] > adjust_desk.low_pos:
            adjust_desk.lower_desk(state)
            update_state(state, time_until_next_working_day())

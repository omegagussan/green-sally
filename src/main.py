#!/usr/bin/python3

import time
import random
from src.working_time import is_working_time
from src.adjust_desk import AdjustDesk
from src.state import get_state

adjust_desk = AdjustDesk()


class StatePositionException(Exception):
    pass


def wait_until_next_operation():
    min = 45  # minutes
    max = 120  # minutes
    return random.randint(min, max) * 60


while True:
    if is_working_time():
        state = get_state()
        if state["position"] == 1:
            adjust_desk.lower_desk()
        elif state["position"] == 0:
            adjust_desk.raise_desk()
        else:
            raise StatePositionException("Unknown position")
    time.sleep(wait_until_next_operation())

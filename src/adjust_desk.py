#!/usr/bin/python3

import time
import RPi.GPIO as GPIO

from src.state import set_state


def apply_operation(pin, duration):
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(pin, GPIO.LOW)


class AdjustDesk:
    def __init__(self):
        self.up = 18
        self.down = 19

        self.raise_time = 10
        self.lower_time = 10

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.up, GPIO.OUT)
        GPIO.setup(self.down, GPIO.OUT)

    def raise_desk(self):
        apply_operation(self.up, self.raise_time)
        set_state({"position": 1})

    def lower_desk(self):
        apply_operation(self.down, self.lower_time)
        set_state({"position": 0})

    def __exit__(self, exc_type, exc_val, exc_tb):
        GPIO.cleanup()

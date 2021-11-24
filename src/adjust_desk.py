#!/usr/bin/python3

import time
import RPi.GPIO as GPIO

from src.state import set_state_value


def apply_operation(pin, duration):
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(pin, GPIO.LOW)


class AdjustDesk:
    def __init__(self):
        self.up = 17
        self.down = 18

        self.raise_time = 12
        self.lower_time = 8

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.up, GPIO.OUT)
        GPIO.setup(self.down, GPIO.OUT)
        GPIO.output(self.down, GPIO.LOW)
        GPIO.output(self.up, GPIO.LOW)
        self.debug()

    def raise_desk(self):
        apply_operation(self.up, self.raise_time)
        set_state_value("position", 1)

    def lower_desk(self):
        apply_operation(self.down, self.lower_time)
        set_state_value("position", 0)

    def debug(self):
        print(f"up is {GPIO.input(self.up)}")
        print(f"down is {GPIO.input(self.down)}")


def __exit__(self, exc_type, exc_val, exc_tb):
    GPIO.cleanup()

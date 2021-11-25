#!/usr/bin/python3

import time
import RPi.GPIO as GPIO

from src.height_sensor import HeightSensor


class AdjustDesk:
    def __init__(self):
        self.up = 17
        self.down = 18

        self.resolution = 1

        self.high_pos = 113  # https://www.healthline.com/nutrition/6-tips-for-using-a-standing-desk
        self.low_pos = 90

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.up, GPIO.OUT)
        GPIO.setup(self.down, GPIO.OUT)
        self.set_idle()
        self.debug()

        self.heightSensor = HeightSensor()

    def threshold(self):
        return (self.high_pos + self.low_pos) / 2

    def raise_desk(self, state):
        condition_function = lambda: self.heightSensor.get() <= self.high_pos
        self.set_idle()
        self.apply_operation(self.up, condition_function, "raising")
        self.set_idle()
        state.set_state_value("position", self.heightSensor.get_smooth())

    def lower_desk(self, state):
        condition_function = lambda: self.heightSensor.get() >= self.low_pos
        self.set_idle()
        self.apply_operation(self.down, condition_function, "lowering")
        self.set_idle()
        state.set_state_value("position", self.heightSensor.get_smooth())

    def set_idle(self):
        GPIO.output(self.down, GPIO.LOW)
        GPIO.output(self.up, GPIO.LOW)

    def debug(self):
        print(f"up is {GPIO.input(self.up)}")
        print(f"down is {GPIO.input(self.down)}")

    def apply_operation(self, pin, condition_function, friendly_log_name=None):
        GPIO.output(pin, GPIO.HIGH)
        while condition_function():
            if friendly_log_name:
                print(friendly_log_name)
            self.debug()
            time.sleep(self.resolution)
        GPIO.output(pin, GPIO.LOW)


def __exit__(self, exc_type, exc_val, exc_tb):
    GPIO.cleanup()

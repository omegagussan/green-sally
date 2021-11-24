#!/usr/bin/python3

import time
import RPi.GPIO as GPIO

from src.height_sensor import HeightSensor


def apply_operation(pin, duration):
    GPIO.output(pin, GPIO.HIGH)
    print("applying")
    time.sleep(duration)
    print("stop")
    GPIO.output(pin, GPIO.LOW)


class AdjustDesk:
    def __init__(self):
        self.up = 17
        self.down = 18

        self.resolution = 3

        self.high_pos = 113  # https://www.healthline.com/nutrition/6-tips-for-using-a-standing-desk
        self.low_pos = 90

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.up, GPIO.OUT)
        GPIO.setup(self.down, GPIO.OUT)
        GPIO.output(self.down, GPIO.LOW)
        GPIO.output(self.up, GPIO.LOW)
        self.debug()

        self.heightSensor = HeightSensor()

    def threshold(self):
        return (self.high_pos + self.low_pos) / 2

    def raise_desk(self, state):
        while self.heightSensor.get() < self.high_pos:
            print("raising")
            print(self.heightSensor.get_smooth())
            apply_operation(self.up, self.resolution)
            state.set_state_value("position", self.heightSensor.get_smooth())

    def lower_desk(self, state):
        while self.heightSensor.get() > self.low_pos:
            print("lowering")
            print(self.heightSensor.get_smooth())
            apply_operation(self.down, self.resolution)
            state.set_state_value("position", self.heightSensor.get_smooth())

    def debug(self):
        print(f"up is {GPIO.input(self.up)}")
        print(f"down is {GPIO.input(self.down)}")


def __exit__(self, exc_type, exc_val, exc_tb):
    GPIO.cleanup()

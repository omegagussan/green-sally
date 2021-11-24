import RPi.GPIO as GPIO
import time
import collections

de = collections.deque([])

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
GPIO_TRIGGER = 27
GPIO_ECHO = 22

# set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


def distance():
    # set Trigger to HIGH after 0.01ms to LOW as a pulse
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    while_start = time.time()
    start_time = time.time()
    stop_time = time.time()

    # save pulse start_time
    while GPIO.input(GPIO_ECHO) == 0:
        timeout = start_time - while_start
        if timeout > 1:
            return None
        start_time = time.time()

    # save pulse end
    while GPIO.input(GPIO_ECHO) == 1:
        timeout = start_time - while_start
        if timeout > 8000 / 34300:
            return 4000
        stop_time = time.time()

    # time difference between puls start and end
    time_elapsed = stop_time - start_time
    # sonic speed (34300 cm/s)
    # divide by 2, because there and back
    d = (time_elapsed * 34300) / 2
    d += 25
    return d


class HeightSensor:
    def __init__(self, memory=4, get_tries=3):
        self.memory = memory
        self.get_tries = get_tries
        self.smooth_state = collections.deque([])

    def get_raw(self):
        dist = distance()
        if dist:
            self._set_smooth(dist, returns=False)
        return dist

    def get(self):
        for _ in range(self.get_tries):
            dist = distance()
            if dist:
                self._set_smooth(dist, returns=False)
        return self.get_smooth()

    def _set_smooth(self, val, returns=True):
        self.smooth_state.appendleft(val)
        if len(self.smooth_state) > self.memory:
            self.smooth_state.pop()
        if not returns:
            return
        return self.get_smooth()

    def get_smooth(self):
        smooth = sum(self.smooth_state) / len(self.smooth_state)
        print(f"smooth {smooth}")
        return smooth
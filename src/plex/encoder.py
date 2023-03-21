import RPi.GPIO as GPIO
import time

SPEED_SCALE = 70/1200

class Encoder:    
    def __init__(self, A, B) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(B, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(A, GPIO.RISING, callback=self.callback)

        self.B = B
        self.steps = 0
        self.time = time.time()
        self.speed = 0
        self.sum_speed = 0
        self.count = 0
    
    def callback(self, channel):
        current_time = time.time()
        self.sum_speed += SPEED_SCALE/(current_time - self.time)
        self.time = current_time
        self.count += 1

        if self.count > 50:
            self.speed = self.sum_speed / self.count
            self.sum_speed = 0
            self.count = 0

        if GPIO.input(self.B):
            self.steps += 1
        else:
            self.steps -= 1

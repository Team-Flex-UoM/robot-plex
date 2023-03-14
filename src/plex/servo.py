import RPi.GPIO as GPIO
import time

class Servo:
    def __init__(self, servoPin):
        self.servoPin = servoPin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.servoPin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.servoPin, 50) # PWM signal at 50Hz
        self.pwm.start(0)

    def set_angle(self, angle):
        duty_cycle = 2 + (angle/18) # calculate duty cycle from angle
        self.pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(0.5)

    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()

    def reset(self):
        self.set_angle(0)
        
    

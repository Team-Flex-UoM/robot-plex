import RPi.GPIO as GPIO
import time

class Servo:
    def __init__(self, servoPin):
        self.servoPin = servoPin
        GPIO.setmode(GPIO.BCM) 
        GPIO.setup(self.servoPin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.servoPin, 50) # PWM signal at 50Hz also depends on the servo
        self.pwm.start(0)

    def set_angle(self, angle): # angle is between 0 and 180, depends on the servo
        duty_cycle = 2 + (angle/18) # calculate duty cycle from angle
        self.pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(0.5)
   
    def reset(self):
        self.set_angle(0)
        time.sleep(0.5)

    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()

    
        
    

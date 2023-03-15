import RPi.GPIO as GPIO
import time

class Servo:
    def __init__(self, servoPin, initialAngle = 0):
        self.servoPin = servoPin
        GPIO.setmode(GPIO.BCM) 
        GPIO.setup(servoPin, GPIO.OUT)
        self.pwm = GPIO.PWM(servoPin, 50) # PWM signal at 50Hz also depends on the servo
        self.pwm.start(0)
        
        self.currentAngle = initialAngle # to track the current angle of the servo
        self.set_angle(initialAngle)

    def set_angle(self, angle): # angle is between 0 and 180, depends on the servo
        if angle > self.currentAngle:
            for i in range(self.currentAngle, angle + 1):
                duty_cycle = 2 + (i/18) # calculate duty cycle from angle
                self.pwm.ChangeDutyCycle(duty_cycle)
                self.currentAngle = i
                time.sleep(0.05) # 50 ms delay --- can change if necessary
        elif angle < self.currentAngle:
            for i in range(self.currentAngle, angle - 1, -1):
                duty_cycle = 2 + (i/18)
                self.pwm.ChangeDutyCycle(duty_cycle)
                self.angle = i
                time.sleep(0.05)
        
       
   
    def reset(self):
        self.set_angle(0)
        self.currentAngle = 0
        time.sleep(0.5)

    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()

    
        
    

import RPi.GPIO as GPIO
import time

class Servo:
    def __init__(self, servoPin, initialAngle = 90):
        self.servoPin = servoPin
        GPIO.setmode(GPIO.BOARD) 
        GPIO.setup(servoPin, GPIO.OUT)
        self.pwm = GPIO.PWM(servoPin, 50) # PWM signal at 50Hz also depends on the servo
        self.pwm.start(0)
        print("Hello 1")
        self.currentAngle = initialAngle # to track the current angle of the servo
        self.set_angle(initialAngle)
        time.sleep(2)

    def set_angle(self, angle): # angle is between 0 and 180, depends on the servo
        print("Turning from "+ str(self.currentAngle) + " to " + str(angle))
        if angle > self.currentAngle:
            for i in range(self.currentAngle, angle + 1, 5):
                duty_cycle = 2 + (i/18) # calculate duty cycle from angle
                self.pwm.ChangeDutyCycle(duty_cycle)
                self.currentAngle = i
                time.sleep(0.05) # 50 ms delay --- can change if necessary
                self.pwm.ChangeDutyCycle(0)
                time.sleep(0.05)
        elif angle < self.currentAngle:
            for i in range(self.currentAngle, angle - 1, -5):
                duty_cycle = 2 + (i/18)
                self.pwm.ChangeDutyCycle(duty_cycle)
                self.currentAngle = i
                time.sleep(0.05)
                self.pwm.ChangeDutyCycle(0)
                time.sleep(0.05)
        

    def set_angle1(self, angle): # angle is between 0 and 180, depends on the servo
        print("Turning from "+ str(self.currentAngle) + " to " + str(angle) + " directly")
        duty_cycle = 2 + (angle/18)
        self.pwm.ChangeDutyCycle(duty_cycle)
        self.currentAngle = angle
        time.sleep(0.3) # 50 ms delay --- can change if necessary
        self.pwm.ChangeDutyCycle(0)
        #time.sleep(0.7)
        
       
   
    def reset(self):
        self.set_angle(90)
        self.currentAngle = 140
        time.sleep(0.5)
        self.pwm.ChangeDutyCycle(0)

    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()



my_servo = Servo(10,140) # Initialize servo on GPIO pin 18 with initial angle of 90 degrees
my_servo.set_angle(60)   # Move servo to 0 degree position gradually
time.sleep(2)           # Pause for 1 second
#my_servo.set_angle(0) # Move servo to 180 degree position gradually
#time.sleep(1)           # Pause for 1 second
my_servo.reset()         # Move servo to 0 degree position immediately
#my_servo.cleanup()      # Stop PWM signal and cleanup GPIO pins



#4.9 cm 80
#

    
        
    

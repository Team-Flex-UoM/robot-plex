import RPi.GPIO as GPIO

DIR_CLKWS=0
DIR_ANTCLKWS=1
FREQUENCY=50 #50Hz
MAX_SPEED = 80
MIN_SPEED = 10

class Motor:    
    def __init__(self, ena, motor_out_A, motor_out_B) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(ena, GPIO.OUT)
        GPIO.setup(motor_out_A, GPIO.OUT)
        GPIO.setup(motor_out_B, GPIO.OUT)

        self.ena=ena
        self.motor_out_A=motor_out_A
        self.motor_out_B=motor_out_B

        self.pwm = GPIO.PWM(motor_out_A, FREQUENCY)

    def set_dir(self, dir) -> None:
        GPIO.output(self.motor_out_B, dir)

    def set_speed(self,speed) -> None:
        self.pwm.start(max(min(speed, MAX_SPEED), MIN_SPEED))

    def brake(self) -> None:
        GPIO.output(self.motor_out_A, 1)
        GPIO.output(self.motor_out_B, 1)

    def stop(self) -> None:
        GPIO.output(self.ena, 0)

    def start(self) -> None:
        GPIO.output(self.ena, 1)
    
    def __del__(self) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup([self.ena, self.motor_out_A, self.motor_out_B])
        
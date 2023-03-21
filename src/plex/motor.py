import RPi.GPIO as GPIO
import plex.encoder as encoder

DIR_CLKWS=0
DIR_ANTCLKWS=1
FREQUENCY=50 #50Hz
MAX_SPEED = 80
MIN_SPEED = 10
KP = 0.5
KI = 0
KD = 0

prev_error = 0
acc_error = 0

class Motor:    
    def __init__(self, ena, motor_out_A, motor_out_B, encoder_node: encoder.Encoder) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(ena, GPIO.OUT)
        GPIO.setup(motor_out_A, GPIO.OUT)
        GPIO.setup(motor_out_B, GPIO.OUT)

        self.ena=ena
        self.motor_out_A=motor_out_A
        self.motor_out_B=motor_out_B
        self.encoder = encoder_node

        self.pwm = GPIO.PWM(motor_out_A, FREQUENCY)
        self.pwm.start(0)      
    
    def pid(self, ref_speed):
        global prev_error
        global acc_error

        error = ref_speed - self.encoder.speed
        out_speed = KP*error + KI*(acc_error + error) + KD*(error - prev_error)
        acc_error += error
        prev_error = error
        print(ref_speed, self.encoder.speed)
        return out_speed

    def set_dir(self, dir) -> None:
        GPIO.output(self.motor_out_B, dir)

    def set_speed(self,speed) -> None:
        self.pwm.ChangeDutyCycle(max(min(speed, MAX_SPEED), MIN_SPEED))

    def stop(self) -> None:
        GPIO.output(self.ena, 0)

    def start(self) -> None:
        GPIO.output(self.ena, 1)
    
    def __del__(self) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup([self.ena, self.motor_out_A, self.motor_out_B])
        
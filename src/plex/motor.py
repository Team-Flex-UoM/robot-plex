import RPi.GPIO as GPIO
DIR_CLKWS=0
DIR_ANTCLKWS=1
FREQUENCY=50 #50Hz

class Motor:    
    def __init__(self,ena,motor_out_A,motor_out_B,enc_in_A,enc_in_B,callback=None) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(ena, GPIO.OUT)
        GPIO.setup(motor_out_A, GPIO.OUT)
        GPIO.setup(motor_out_B, GPIO.OUT)
        GPIO.setup(enc_in_A, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Enables the internal pull-down resistor
        GPIO.setup(enc_in_B, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Enables the internal pull-down resistor

        # #call '_transitionOccurred' function whenever there is a transition (either from high to low or low to high) on the encoder input
        # GPIO.add_event_detect(enc_in_A, GPIO.BOTH, callback=self._transitionOccurred)
        # GPIO.add_event_detect(enc_in_B, GPIO.BOTH, callback=self._transitionOccurred)

        self.ena=ena
        self.motor_out_A=motor_out_A
        self.motor_out_B=motor_out_B
        self.pwm = GPIO.PWM(motor_out_A, FREQUENCY)
        self.enc_in_A=enc_in_A
        self.enc_in_B=enc_in_B
        self.pos=0
        self.state='00'
        self.callback=callback

        GPIO.output(self.ena,0)


    
    def _transitionOccurred(self,channel):
        p1 = GPIO.input(self.enc_in_A)
        p2 = GPIO.input(self.enc_in_B)
        newState = "{}{}".format(p1, p2)

        if self.state == "00": # Resting position
            if newState == "01": # Turned right 1
                self.pos += 1
            elif newState == "10": # Turned left 1
                self.pos -= 1

        elif self.state == "01": # R1 or L3 position
            if newState == "11": # Turned right 1
                self.pos += 1
            elif newState == "00": # Turned left 1
                self.pos -= 1
                if self.callback is not None:
                    self.callback(self.pos)

        elif self.state == "10": # R3 or L1
            if newState == "11": # Turned left 1
                self.pos -= 1
            elif newState == "00": # Turned right 1
                self.pos += 1
                if self.callback is not None:
                    self.callback(self.pos)

        else: # self.state == "11"
            if newState == "01": # Turned left 1
                self.pos -= 1
            elif newState == "10": # Turned right 1
                self.pos += 1
                
        self.state = newState

    def set_dir(self,dir):
        if dir==DIR_CLKWS:
            GPIO.output(self.motor_out_B,0)
        elif dir==DIR_ANTCLKWS:
            GPIO.output(self.motor_out_B,1)

    def set_speed(self,speed=0) -> None:
        # GPIO.output(self.ena, 1)
        self.pwm.start(speed)

    def brake(self) -> None:
        GPIO.output(self.motor_out_A,1)
        GPIO.output(self.motor_out_B,1)

    def stop(self) -> None:
        GPIO.output(self.ena,0)

    def start(self) -> None:
        GPIO.output(self.ena,1)

    def reset_steps(self) -> None:
        self.pos=0

    def get_steps(self) -> None:
        return self.pos
    
    def __del__(self):
        print('fe')
        
        
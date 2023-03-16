DIR_CLKWS=0
DIR_ANTCLKWS=1

class Motor:
    

    def __init__(self, motor_out_A=None,motor_out_B=None,enc_in_A=None,enc_in_B=None,_robot=None,motor_name=None,enc_name=None) -> None:
        self.motor=_robot.getDevice(motor_name)        
        self.enc=_robot.getDevice(enc_name)
        self.enc.enable(int(_robot.getBasicTimeStep()))
        self.enc.steps=self.enc.getValue()       

    def set_dir(self,dir):
        self.dir=dir        

    def set_speed(self,speed) -> None:
        self.speed=speed

    def brake(self) -> None:
        self.motor.setVelocity(0)

    def stop(self) -> None:
        self.motor.setVelocity(0)

    def start(self) -> None:
        self.motor.setPosition(float('inf'))       
        if self.dir==DIR_CLKWS:
            self.motor.setVelocity(self.speed)
        elif self.dir==DIR_ANTCLKWS:
            self.motor.setVelocity(-self.speed)

    def reset_steps(self) -> None:
        self.enc.steps=self.enc.getValue()

    def get_steps(self) -> None:
        return self.enc.getValue()-self.enc.steps


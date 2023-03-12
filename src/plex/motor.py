DIR_CLKWS=0
DIR_ANTCLKWS=1
class Motor:    
    def __init__(self, motor_out1,motor_out2,enc_in) -> None:
        self.motor_out1=motor_out1
        self.motor_out2=motor_out2
        self.enc_in=enc_in
        pass

    def set_dir(dir):
        pass

    def set_speed(speed) -> None:
        pass

    def brake() -> None:
        pass

    def stop() -> None:
        pass

    def start() -> None:
        pass

    def reset_steps() -> None:
        pass

    def get_steps() -> None:
        pass

    
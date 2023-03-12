DIR_CLKWS=0
DIR_ANTCLKWS=1
class Motor:    
    def __init__(self, motor_out_A,motor_out_B,enc_in_A,enc_in_B) -> None:
        self.motor_out_A=motor_out_A
        self.motor_out_B=motor_out_B
        self.enc_in_A=enc_in_A
        self.enc_in_B=enc_in_B
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


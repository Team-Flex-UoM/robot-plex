import plex.motor as motor

MAX_SPEED = 80
MIN_SPEED = 10

def init(left_motor_node: motor.Motor, right_motor_node: motor.Motor) -> None:
    global left_motor
    global right_motor
    left_motor, right_motor = left_motor_node, right_motor_node

def forward(left_motor_speed, right_motor_speed) -> None:
    left_motor.set_dir(motor.DIR_CLKWS)
    right_motor.set_dir(motor.DIR_CLKWS)

    left_motor.set_speed(speed=max(min(left_motor_speed, MAX_SPEED), MIN_SPEED))
    right_motor.set_speed(speed=max(min(right_motor_speed, MAX_SPEED), MIN_SPEED))

    left_motor.start()
    right_motor.start()
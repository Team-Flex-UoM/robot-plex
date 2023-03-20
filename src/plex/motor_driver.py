import plex.motor as motor
from gpiozero import RotaryEncoder

TURN_SPEED = 15
TURN_ENC_COUNT = 100

def init(left_motor_node: motor.Motor, right_motor_node: motor.Motor, left_encoder_node: RotaryEncoder, right_encoder_node: RotaryEncoder) -> None:
    global left_motor
    global right_motor
    global left_encoder
    global right_encoder

    left_motor = left_motor_node
    right_motor = right_motor_node
    left_encoder = left_encoder_node
    right_encoder = right_encoder_node

def forward(left_motor_speed, right_motor_speed) -> None:
    left_motor.set_dir(motor.DIR_CLKWS)
    right_motor.set_dir(motor.DIR_CLKWS)
    left_motor.set_speed(left_motor_speed)
    right_motor.set_speed(right_motor_speed)
    left_motor.start()
    right_motor.start()

def turn_left() -> None:
    left_motor.set_dir(motor.DIR_CLKWS)
    right_motor.set_dir(motor.DIR_CLKWS)
    left_motor.set_speed(TURN_SPEED)
    right_motor.set_speed(TURN_SPEED)
    right_encoder.steps = 0
    left_motor.start()
    right_motor.start()
    while right_encoder.steps <= TURN_ENC_COUNT:
        continue
    left_motor.stop()
    right_motor.stop()

    
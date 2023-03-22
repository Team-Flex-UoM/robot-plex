import plex.motor as motor
from gpiozero import RotaryEncoder
from time import sleep

AHEAD=0
LEFT = 1
RIGHT = 2
BACK=3

TURN_SPEED = 15
TURN_ENC_COUNT = 100

is_running = False

def init(left_motor_node: motor.Motor, right_motor_node: motor.Motor) -> None:
    global left_motor
    global right_motor

    left_motor = left_motor_node
    right_motor = right_motor_node


def forward(left_motor_speed, right_motor_speed) -> None:
    kick(AHEAD)
    left_motor.set_speed(left_motor_speed)
    right_motor.set_speed(right_motor_speed)
    left_motor.start()
    right_motor.start()

def backward(left_motor_speed, right_motor_speed) -> None:
    kick(BACK)
    left_motor.set_speed(left_motor_speed)
    right_motor.set_speed(right_motor_speed)
    left_motor.start()
    right_motor.start()

# def turn(dir: int) -> None:
#     if dir == LEFT:
#         left_motor.set_dir(motor.DIR_ANTCLKWS)
#         right_motor.set_dir(motor.DIR_CLKWS)
#     else:
#         left_motor.set_dir(motor.DIR_ANTCLKWS)
#         right_motor.set_dir(motor.DIR_CLKWS)
    
#     left_motor.set_speed(TURN_SPEED)
#     right_motor.set_speed(TURN_SPEED)
#     right_encoder.steps = 0
#     left_motor.start()
#     right_motor.start()
#     while right_encoder.steps <= TURN_ENC_COUNT:
#         continue
#     left_motor.stop()
#     right_motor.stop()

# def go_distance(dis: int):
#     if dir > 0:
#         left_motor.set_dir(motor.DIR_ANTCLKWS)
#         right_motor.set_dir(motor.DIR_ANTCLKWS)
#     else:
#         left_motor.set_dir(motor.DIR_CLKWS)
#         right_motor.set_dir(motor.DIR_CLKWS)
    
#     left_motor.set_speed(TURN_SPEED)
#     right_motor.set_speed(TURN_SPEED)
#     right_encoder.steps = 0
#     left_motor.start()
#     right_motor.start()
#     while right_encoder.steps <= TURN_ENC_COUNT:
#         continue
#     left_motor.stop()
#     right_motor.stop()


def kick(dir: int) -> None:
    global is_running

    if is_running: return

    is_running=True

    if dir == AHEAD:
        left_motor.set_dir(motor.DIR_ANTCLKWS)
        right_motor.set_dir(motor.DIR_CLKWS)
    elif dir == LEFT:
        left_motor.set_dir(motor.DIR_CLKWS)
        right_motor.set_dir(motor.DIR_CLKWS)
    elif dir ==RIGHT:
        left_motor.set_dir(motor.DIR_ANTCLKWS)
        right_motor.set_dir(motor.DIR_ANTCLKWS)
    else:
        left_motor.set_dir(motor.DIR_CLKWS)
        right_motor.set_dir(motor.DIR_ANTCLKWS)
    
    left_motor.set_speed(50)
    right_motor.set_speed(50)
    left_motor.start()    
    right_motor.start()
    sleep(0.4)

def stop():
    left_motor.stop()
    right_motor.stop()
    is_running=False

    
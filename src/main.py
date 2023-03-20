import plex.camera as camera
import plex.motor as motor
import plex.line_follow as line_follow
import plex.motor_driver as motor_driver
from gpiozero import RotaryEncoder
import cv2
from time import sleep

# Robot nodes
cam = camera.Camera()
left_motor = motor.Motor(2, 18, 3)
right_motor = motor.Motor(26, 12, 16)
left_encoder = RotaryEncoder(a=4, b=14, bounce_time=0.0005, max_steps=0)
right_encoder = RotaryEncoder(a=20, b=21, bounce_time=0.0005, max_steps=0)

# initializations
line_follow.init(cam)
motor_driver.init(left_motor, right_motor, left_encoder, right_encoder)

# while(True):
#     frame = line_follow.follow()
#     # cv2.imshow('frame', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
    

# cv2.destroyAllWindows()
# line_follow.test()
    
motor_driver.turn_left()



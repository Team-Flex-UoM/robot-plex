import plex.camera as camera
import plex.motor as motor
import plex.line_follow as line_follow
import plex.motor_driver as motor_driver
import cv2
from time import sleep

# Robot nodes
cam = camera.Camera()
left_motor = motor.Motor(2, 18, 3, 4, 14)
right_motor = motor.Motor(26, 12, 16, 20, 21)

# initializations
line_follow.init(cam_node=cam)
motor_driver.init(left_motor_node=left_motor, right_motor_node=right_motor)

while(True):
    frame = line_follow.follow()
    # cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

cv2.destroyAllWindows()
# line_follow.test()
    


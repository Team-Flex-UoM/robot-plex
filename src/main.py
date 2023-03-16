from plex.camera import Camera
import plex.motor as motor
import plex.line_follow as line_follow
import cv2
from time import sleep
# Robot nodes

# initializations
# line_follow.init(cam)


left_motor.set_dir(motor.DIR_CLKWS)
left_motor.set_speed(10)
sleep(5)  
left_motor.stop()
    

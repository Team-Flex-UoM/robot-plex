from plex.camera import Camera
import plex.motor as motor
import plex.line_follow as line_follow
import cv2
from time import sleep
# Robot nodes
# cam = Camera()
left_motor = motor.Motor(ena=2, motor_out_A=18, motor_out_B=4, enc_in_A=17, enc_in_B=27)

# initializations
# line_follow.init(cam)


left_motor.set_dir(motor.DIR_CLKWS)
left_motor.set_speed(10)
sleep(5)  
left_motor.stop()
    

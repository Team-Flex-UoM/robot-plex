"""plex_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
# from plex.motor import Motor
import plex.motor as motor
from plex.motor import Motor

import plex.camera as camera
from plex.camera import Camera



import cv2
import numpy as np


# # create the Robot instance.
robot = Robot()
motorLeft=Motor(_robot=robot,motor_name="leftMotor",enc_name="leftEncoder")
motorLeft.set_dir(motor.DIR_CLKWS)
motorLeft.set_speed(10)
motorLeft.start()

cam=Camera(robot)

print("hello")

# # get the time step of the current world.
timestep = int(robot.getBasicTimeStep())


# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:

    # # get image
    
    image_in_bgr=cam.get_frame()

    image_edit=cv2.circle(image_in_bgr,(cam.imageWidth//2,cam.imageHeight//2),min(cam.imageHeight,cam.imageWidth)//4,(26,181,0),2)

    cam.show_frame(image_edit)
    
    pass

# Enter here exit cleanup code.



while robot.step(timestep) != -1:pass



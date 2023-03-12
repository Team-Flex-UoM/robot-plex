"""plex_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot,Camera,Display

import cv2
import numpy as np

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())


camera=robot.getDevice("camera")
camera.enable(timestep)
imageWidth=camera.getWidth()
imageHeight=camera.getHeight()
display=robot.getDevice("display")

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:

    # # get image
    
    image_in_raw=camera.getImage()  
    image_in_list=list(image_in_raw)
    image_in_arr=np.array(image_in_list,dtype=np.uint8)
    image_in_bgra=np.reshape(image_in_arr,(imageHeight,imageWidth,4)) # image format : BGRA
    # image=np.reshape(image_in_arr,(imageHeight,imageWidth,4)) [:,:,:-1]  # image format : BGR
    image_in_bgr=cv2.cvtColor(image_in_bgra,cv2.COLOR_BGRA2BGR)
    # # process image

    image_edit=cv2.circle(image_in_bgr,(imageWidth//2,imageHeight//2),min(imageHeight,imageWidth)//4,(26,181,0),2)

    # image_bw=cv2.cvtColor(image_edit,cv2.COLOR_BGRA2GRAY)

    # image_edit=cv2

    # # display image

    image_out_bgr=cv2.cvtColor(image_edit,cv2.COLOR_BGR2BGRA)
    image_out_arr=image_out_bgr.flatten()
    image_out_list=list(image_out_arr)    
    image_out_raw=bytes(image_out_list)
    ir=display.imageNew(image_out_raw,Display.BGRA,imageWidth,imageHeight)
    display.imagePaste(ir,0,0,False)
    display.imageDelete(ir)
    
    pass

# Enter here exit cleanup code.

# import plex.line_follow as line_follow
# import plex.camera as camera
# from plex.camera import Camera
# import cv2

# cam = Camera()
# # initializations
# line_follow.init(cam)
# while True:
#     # roi,img=line_follow.get_roi()
#     # frame=line_follow.process_roi(roi)
#     # cv2.circle(roi,(2,2),3,(0,255,0),3)
#     # frame=cam.get_,frame()
   
#     # cv2.imshow('img',img)
#     # cv2.imshow('roi',roi)
#     # cv2.imshow('frame',frame)

#     line_follow.follow()

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# cv2.destroyAllWindows()


import plex.motor as motor
import plex.motor_driver as motor_driver
import plex.line_follow as line_follow
import plex.camera as camera
from gpiozero import RotaryEncoder
from time import sleep,time
import cv2

left_motor = motor.Motor(26, 12, 16)
right_motor = motor.Motor(2, 18, 3)
left_encoder = RotaryEncoder(20, 21, bounce_time=0.0005, max_steps=0)
right_encoder = RotaryEncoder(4, 14, bounce_time=0.0005, max_steps=0)
cam = camera.Camera()

motor_driver.init(left_motor, right_motor, left_encoder, right_encoder)
line_follow.init(cam)

while True:
    line_follow.test()
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cv2.destroyAllWindows()

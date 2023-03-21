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
from plex.encoder import Encoder
import plex.motor_driver as motor_driver
from time import sleep,time
en = Encoder(20, 21)
en1 = Encoder(4,14)
left_motor = motor.Motor(26, 12, 16, en)
right_motor = motor.Motor(2, 18, 3, en1)

motor_driver.init(left_motor, right_motor)

motor_driver.backward(30,30)


while True:
    # left_motor.set_speed(50)
    # left_motor.start()
    # right_motor.set_speed(50)
    # right_motor.start()
    pass



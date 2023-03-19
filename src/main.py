import plex.camera as camera
import plex.motor as motor
import plex.line_follow as line_follow
import plex.motor_driver as motor_driver

import RPi.GPIO as GPIO
import cv2
from time import sleep

# Robot nodes
cam = camera.Camera()
left_motor = motor.Motor(2, 18, 3, 4, 14)
right_motor = motor.Motor(26, 12, 16, 20, 21)

# initializations
line_follow.init(cam_node=cam)
motor_driver.init(left_motor_node=left_motor, right_motor_node=right_motor)

i=0
while(True):
    frame = cam.get_frame()
    cv2.imshow('frame', frame)
    # cv2.imwrite('imgs/{}.png'.format(i),frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite('{}.png'.format(i),frame)
        i+=1
        print(i)
      
    
    # sleep(2)
cv2.destroyAllWindows()
    


# line_follow.test()
    

# motor_driver.forward(15, 15)
# sleep(2)
# GPIO.cleanup()

# line_follow.test()
# cam.record()

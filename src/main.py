import plex.camera as camera
import plex.motor as motor
import plex.line_follow as line_follow
import plex.motor_driver as motor_driver

import RPi.GPIO as GPIO
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

# i=0
# while(True):
#     frame = cam.get_frame()
#     cv2.imshow('frame', frame)
#     # cv2.imwrite('imgs/{}.png'.format(i),frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         cv2.imwrite('{}.png'.format(i),frame)
#         i+=1
#         print(i)
      
    
#     # sleep(2)
# cv2.destroyAllWindows()
    


# line_follow.test()
    
motor_driver.turn_left()


# motor_driver.forward(15, 15)
# sleep(2)
# GPIO.cleanup()

# line_follow.follow()
# cam.record()

# i=0
try:
    while(True):
        line_follow.follow()
except KeyboardInterrupt: pass
    

# left_motor.set_dir(motor.DIR_ANTCLKWS)
# print("set dir")
# sleep(2)
# left_motor.set_speed(20)
# print("set speed")
# sleep(2)
# left_motor.start()
# print("start")
# sleep(2)
# left_motor.stop()
# print("stop")

# right_motor.set_dir(motor.DIR_ANTCLKWS)
# print("set dir")
# sleep(2)
# right_motor.set_speed(20)
# print("set speed")
# sleep(2)
# right_motor.start()
# print("start")
# sleep(2)
# right_motor.stop()
# print("stop")

# motor_driver.forward(20,20)



# input()
# while :pass

GPIO.cleanup()    
# cv2.destroyAllWindows()
    

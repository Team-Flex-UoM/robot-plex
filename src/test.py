import RPi.GPIO as GPIO
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

# motor_driver.init(left_motor, right_motor, left_encoder, right_encoder)
line_follow.init(cam)
try:
    while True:        
        line_follow.test()
        #frame=cam.get_frame()
        # print(frame.shape)
        # cv2.imshow("a",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except:
    GPIO.cleanup()
cv2.destroyAllWindows()

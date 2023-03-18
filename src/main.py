import plex.camera as camera
import plex.motor as motor
import plex.line_follow as line_follow
import cv2
from time import sleep

# Robot nodes
cam = camera.Camera()

# initializations
line_follow.init(cam)

while(True):
    frame = line_follow.test()
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

cv2.destroyAllWindows()
# line_follow.test()
    


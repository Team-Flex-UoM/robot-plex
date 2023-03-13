from plex.camera import Camera
from plex.motor import Motor
import plex.line_follow as line_follow
import cv2

# Robot nodes
cam = Camera()

# initializations
line_follow.init(cam)

while(True):
    frame = line_follow.get_line_mask()
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

cv2.destroyAllWindows()
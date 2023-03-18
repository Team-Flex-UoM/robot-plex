import plex.line_follow as line_follow
import plex.camera as camera
from plex.camera import Camera
import cv2

cam = Camera()
# initializations
line_follow.init(cam)
while True:
    frame=line_follow.process_roi()
    # frame=cam.get_frame()
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
import plex.line_follow as line_follow
import plex.camera as camera
from plex.camera import Camera
import cv2

cam = Camera()
# initializations
line_follow.init(cam)
while True:
    roi,img=line_follow.get_roi()
    frame=line_follow.process_roi(roi)
    # frame=cam.get_frame()
    cv2.imshow('frame',roi)
    cv2.imshow('frame2',img)
    cv2.imshow('frame3',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
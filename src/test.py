import plex.line_follow as line_follow
import plex.camera as camera
from plex.camera import Camera
import cv2

cam = Camera()
# initializations
line_follow.init(cam)
while True:
    # roi,img=line_follow.get_roi()
    # frame=line_follow.process_roi(roi)
    # cv2.circle(roi,(2,2),3,(0,255,0),3)
    # frame=cam.get_,frame()
   
    # cv2.imshow('img',img)
    # cv2.imshow('roi',roi)
    # cv2.imshow('frame',frame)

    line_follow.follow()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
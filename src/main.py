import plex.camera as camera
import cv2

# init
cam = camera.Camera()

while(True):
    frame = cam.get_mask_frame(camera.WHITE)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

cv2.destroyAllWindows()
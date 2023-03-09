import camera as cam
import cv2

# init
camera = cam.Camera()

while(True):
    frame = camera.get_mask_frame(cam.WHITE)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

cv2.destroyAllWindows()
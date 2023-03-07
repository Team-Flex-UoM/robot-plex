from camera import Camera
import cv2

# init
camera = Camera()

while(True):
    frame = camera.get_frame()
    
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
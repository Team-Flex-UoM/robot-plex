import cv2
import numpy as np

import plex.camera as camera
from plex.camera import Camera
import plex.motor_driver as motor_driver



BOX = (camera.WIDTH//2, camera.HEIGHT//2, 320, 100) # (x,y,w,h)

BOX_X,BOX_Y,BOX_WIDTH,BOX_HEIGHT=BOX
BOX_HALF_WIDTH=BOX_WIDTH//2
BOX_HALF_HEIGHT=BOX_HEIGHT//2

AVG_SPEED = 50
KP = 0
KI = 0
KD = 0

prev_error = 0
acc_error = 0

def init(cam_node: Camera) -> None:
    global cam
    cam = cam_node

def get_bin_frame(frame: np.ndarray) -> np.ndarray:
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, bin_frame = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # morphology
    bin_frame = cv2.morphologyEx(bin_frame, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT,(5,5)))
    bin_frame = cv2.morphologyEx(bin_frame, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT,(5,5)))
    return bin_frame

def get_line_contour(frame: np.ndarray) -> np.ndarray:
    bin_frame = get_bin_frame(frame)
    contours, _ = cv2.findContours(bin_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    max_contour = max(contours, key = cv2.contourArea)
    # print(max_contour)
    return max_contour,bin_frame

# def get_intersection(frame: )



def get_point(conts: np.ndarray, _axis: int):    
    return (np.amin(conts,axis=_axis)+np.amax(conts,axis=_axis))//2

def get_roi():
    img = cam.get_frame()
    # print(img.shape)
    roi = np.array(img[BOX[1] - BOX[3]//2: BOX[1] + BOX[3]//2, BOX[0] - BOX[2]//2: BOX[0] + BOX[2]//2, :])
    img=cv2.rectangle(img,(BOX_X-BOX_HALF_WIDTH,BOX_Y-BOX_HALF_HEIGHT),(BOX_X+BOX_HALF_WIDTH,BOX_Y+BOX_HALF_HEIGHT),(255,0,0),3)

    img=cv2.circle(img,(BOX_X,BOX_Y),3,(0,0,255),3)
    return roi,img


def process_roi(roi: np.ndarray):    
    
    conts,frame = get_line_contour(roi)
    conts = conts.reshape(conts.shape[0], -1)

    left_edge = conts[conts[:, 1] < 2].size
    
    # left_edge_line,left_edge_point=get_point(left_edge,0)

    right_edge=conts[conts[:, 1] > (BOX_WIDTH-3)].size
    # right_edge_line,right_edge_point=get_point(right_edge,0)

    top_edge= conts[conts[:, 0] < 2].size

    bottom_edge_points=conts[conts[:, 0] > (BOX_HEIGHT-3)]
    bottom_edge=bottom_edge_points.size

    if bottom_edge:        
       
        if top_edge and left_edge and right_edge:
            print("+ junction")
        elif left_edge and right_edge:
            print("T junction")
        elif left_edge:
            print("turn left")
        elif right_edge:
            print("turn right")
        else:
            bottom_edge_mid_point=get_point(bottom_edge_points,1)
            error=bottom_edge_mid_point-BOX_HALF_WIDTH
            norm_error=error/BOX_HALF_WIDTH



    else:
        # missed the line
        pass

    return frame

    # if len(arr) > 0:
    #     cv2.circle(img, arr[0], 2,(255,0,0),3)
    # print(img.shape)

    # left edge





def pid(error: int) -> None:
    global prev_error
    global acc_error

    correction = KP*error + KI*(acc_error + error) + KD*(error - prev_error)
    acc_error += error
    prev_error = error

    left_motor_velo = AVG_SPEED + correction
    right_motor_velo = AVG_SPEED - correction

    motor_driver.forward(left_motor_speed=left_motor_velo, right_motor_speed=right_motor_velo)


def test():
    img = cam.get_frame()
    img = img[BOX[1] - BOX[3]//2: BOX[1] + BOX[3]//2, BOX[0] - BOX[2]//2: BOX[0] + BOX[2]//2, :]
    return img

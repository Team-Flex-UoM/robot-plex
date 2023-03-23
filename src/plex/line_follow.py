import cv2
import numpy as np

import plex.camera as camera
from plex.camera import Camera
import plex.motor_driver as motor_driver



BOX = (camera.WIDTH//2, camera.HEIGHT//3, 4*camera.WIDTH//5, 8) # (x,y,w,h)

BOX_X,BOX_Y,BOX_WIDTH,BOX_HEIGHT=BOX
BOX_HALF_WIDTH=BOX_WIDTH//2
BOX_HALF_HEIGHT=BOX_HEIGHT//2
LEFT_POINT = BOX_WIDTH//5
RIGHT_POINT = 4*BOX_WIDTH//5

LINE_EXIST = 0
JUNCTN_L_LEFT = 1
JUNCTN_L_RIGHT = 2
JUNCTN_T = 3
LINE_END = 4

AVG_SPEED = 30
KP = 60
KI = 0
KD = 0

prev_error = 0
acc_error = 0

def init(cam_node: Camera) -> None:
    global cam
    cam = cam_node

def get_bin_frame(frame: np.ndarray) -> np.ndarray:
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, bin_frame = cv2.threshold(gray_frame, 100, 255, cv2.THRESH_BINARY)

    # morphology
    bin_frame = cv2.morphologyEx(bin_frame, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT,(3,3)))
    bin_frame = cv2.morphologyEx(bin_frame, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT,(3,3)))
    return bin_frame

def get_line_contour(frame: np.ndarray) -> np.ndarray:
    bin_frame = get_bin_frame(frame)
    conts, _ = cv2.findContours(bin_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(conts):
        max_cont = max(conts, key = cv2.contourArea) 
        return True,max_cont,bin_frame
    return False,None,bin_frame

# def get_intersection(frame: )

def get_point(conts: np.ndarray, _axis: int):
    left_point = np.amin(conts,axis=_axis)[0]
    right_point = np.amax(conts,axis=_axis)[0]
    mid_point = (left_point + right_point)//2
    return left_point, mid_point, right_point

def get_roi():
    img = cam.get_frame()
    # print(img.shape)
    roi = img[BOX[1] - BOX[3]//2: BOX[1] + BOX[3]//2, BOX[0] - BOX[2]//2: BOX[0] + BOX[2]//2, :]
    img=cv2.rectangle(img,(BOX_X-BOX_HALF_WIDTH,BOX_Y-BOX_HALF_HEIGHT),(BOX_X+BOX_HALF_WIDTH,BOX_Y+BOX_HALF_HEIGHT),(255,0,0),1)

    img=cv2.circle(img,(BOX_X,BOX_Y),1,(0,0,255),1)
    return roi,img

def draw_points(img,points):
    for point in points:
        cv2.circle(img,point,1,(0,255,0),1)

def process_roi(roi: np.ndarray):    
    is_cont,max_cont,bin_frame = get_line_contour(roi)

    if is_cont:
        max_cont = max_cont.reshape(max_cont.shape[0], -1)

        # top_edge = max_cont[max_cont[:, 1] < 2]
        # draw_points(roi,top_edge)

        bottom_edge=max_cont[max_cont[:, 1] > (BOX_HEIGHT-3)]
        # draw_points(roi,bottom_edge)

        # left_edge= max_cont[max_cont[:, 0] < 2]
        # draw_points(roi,left_edge)
        
        # right_edge=max_cont[max_cont[:, 0] > (BOX_WIDTH-3)]
        # draw_points(roi,right_edge)
   
        if bottom_edge.size:
            left_point = np.amin(bottom_edge,axis=0)[0]
            right_point = np.amax(bottom_edge,axis=0)[0]
            mid_point = (left_point + right_point)//2 
            left_point_exist = left_point < LEFT_POINT
            right_point_exist = right_point > RIGHT_POINT
            # draw_points(roi, [left_point, right_point, mid_point])   
        
            if (not left_point_exist) and (not right_point_exist):
                error = mid_point - BOX_HALF_WIDTH
                norm_error = error/BOX_HALF_WIDTH 
                return LINE_EXIST, bin_frame, norm_error 
            elif (left_point_exist) and (right_point_exist):
                return JUNCTN_T, bin_frame, None
            elif (left_point_exist) and (not right_point_exist):
                return JUNCTN_L_LEFT, bin_frame, None
            else:
                return JUNCTN_L_RIGHT, bin_frame, None
            # cv2.circle(roi,top_edge_mid_point,1,(0,255,255),1)
             
        else:
            # TODO : Handle end of miss the line with checking otsu thresold
            return LINE_END, bin_frame, None
    else:
        # TODO : Handle end of miss the line with checking otsu thresold
        return LINE_END, bin_frame, None

def pid(error: int) -> None:
    global prev_error
    global acc_error

    correction = KP*error + KI*(acc_error + error) + KD*(error - prev_error)
    acc_error += error
    prev_error = error

    left_motor_velo = AVG_SPEED + correction
    right_motor_velo = AVG_SPEED - correction

    print("L:",left_motor_velo,"\t, R:",right_motor_velo,"er:",error)

    motor_driver.forward(left_motor_speed=left_motor_velo, right_motor_speed=right_motor_velo)


def test():
    roi,img=get_roi()
    junctn,bin_frame,norm_error=process_roi(roi)
    print(junctn, norm_error)
    # if junctn>=0:
    #     pid(norm_error)
    # else:
    #     print("line miss")
    cv2.imshow('img',img)
    cv2.imshow('roi',roi)
    cv2.imshow('frame',bin_frame)

def follow():
    roi,img=get_roi()

    while True:
        junctn,bin_frame,norm_error=process_roi(roi)
        if junctn>0:break
        pid(norm_error)
        # cv2.imshow('img',img)
        # cv2.imshow('roi',roi)
        # cv2.imshow('frame',bin_frame)

    return junctn

    
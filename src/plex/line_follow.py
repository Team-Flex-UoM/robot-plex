import cv2
import numpy as np

import plex.camera as camera
from plex.camera import Camera
import plex.motor_driver as motor_driver



BOX = (camera.WIDTH//2, camera.HEIGHT//3, 4*camera.WIDTH//5, 8) # (x,y,w,h)

BOX_X,BOX_Y,BOX_WIDTH,BOX_HEIGHT=BOX
BOX_HALF_WIDTH=BOX_WIDTH//2
BOX_HALF_HEIGHT=BOX_HEIGHT//2

COLOR_PATCH_THRES=255*BOX_WIDTH*BOX_HEIGHT//2

JUNCTN_NONE=0
JUNCTN_L_LEFT=1
JUNCTN_L_RIGHT=2

JUNCTN_T_NORM=3
JUNCTN_T_LEFT=4
JUNCTN_T_RIGHT=5

JUNCTN_CROSS=6
JUNCTN_END=7

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
    ret, bin_frame = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

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
    return (np.amin(conts,axis=_axis)+np.amax(conts,axis=_axis))//2

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

        top_edge = max_cont[max_cont[:, 1] < 2]
        draw_points(roi,top_edge)

        bottom_edge=max_cont[max_cont[:, 1] > (BOX_HEIGHT-3)]
        # draw_points(roi,bottom_edge)

        left_edge= max_cont[max_cont[:, 0] < 2]
        # draw_points(roi,left_edge)
        
        right_edge=max_cont[max_cont[:, 0] > (BOX_WIDTH-3)]
        # draw_points(roi,right_edge)
   
        if top_edge.size:        
        
            # if top_edge.size and left_edge.size and right_edge.size:
            #     # print("+")
            #     return JUNCTN_CROSS,bin_frame,None
            #     pass
            # elif top_edge.size and left_edge.size:
            #     # print("TL")
            #     return JUNCTN_T_LEFT,bin_frame,None
            #     pass
            # elif top_edge.size and right_edge.size:
            #     # print("TR")
            #     return JUNCTN_T_RIGHT,bin_frame,None
            #     pass
            # elif left_edge.size and right_edge.size:
            #     # print("TN")
            #     return JUNCTN_T_NORM,bin_frame,None
            #     pass
            # elif left_edge.size:
            #     # print("L")
            #     return JUNCTN_L_LEFT,bin_frame,None
            #     pass
            # elif right_edge.size:
            #     # print("R")
            #     return JUNCTN_L_RIGHT,bin_frame,None
            #     pass
            # elif top_edge.size:            
            #     bottom_edge_mid_point=get_point(bottom_edge,0)
            #     error=bottom_edge_mid_point[0]-BOX_HALF_WIDTH
            #     norm_error=error/BOX_HALF_WIDTH
            #     # print(norm_error)
            #     cv2.circle(roi,bottom_edge_mid_point,3,(0,255,255),3)
            #     return JUNCTN_NONE,bin_frame,norm_error
            # else:
            #     return JUNCTN_END,bin_frame,None

            # only for pid tune
            top_edge_mid_point=get_point(top_edge,0)
            error=top_edge_mid_point[0]-BOX_HALF_WIDTH
            norm_error=error/BOX_HALF_WIDTH            
            # cv2.circle(roi,top_edge_mid_point,1,(0,255,255),1)
            return JUNCTN_NONE,bin_frame,norm_error 
        else:
        # TODO : Handle end of miss the line with checking otsu thresold
            return -1,bin_frame,None   

    else:
        # TODO : Handle end of miss the line with checking otsu thresold
        return -1,bin_frame,None


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
    if junctn>=0:
        pid(norm_error)
    else:
        print("line miss")
    # cv2.imshow('img',img)
    # cv2.imshow('roi',roi)
    # cv2.imshow('frame',bin_frame)

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

    
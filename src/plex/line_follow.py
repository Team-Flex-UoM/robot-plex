import cv2
import numpy as np

import plex.camera as camera
from plex.camera import Camera
import plex.motor_driver as motor_driver



BOX = (camera.WIDTH//2, 3*camera.HEIGHT//5, camera.WIDTH, 200) # (x,y,w,h)

BOX_X,BOX_Y,BOX_WIDTH,BOX_HEIGHT=BOX
BOX_HALF_WIDTH=BOX_WIDTH//2
BOX_HALF_HEIGHT=BOX_HEIGHT//2

AVG_SPEED = 12
KP = 5
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
    if len(contours):
        max_contour = max(contours, key = cv2.contourArea) # TODO : check is empty conts
        return 1,max_contour,bin_frame
    return 0,0,bin_frame

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

def draw_points(img,points):
    for point in points:
        cv2.circle(img,point,3,(0,255,0),3)



def process_roi(roi: np.ndarray):    
    
    is_max_cont,max_cont,bin_frame = get_line_contour(roi)

    if is_max_cont:
        max_cont = max_cont.reshape(max_cont.shape[0], -1)

        top_edge = max_cont[max_cont[:, 1] < 2]
        # draw_points(roi,top_edge)
        
        

        bottom_edge=max_cont[max_cont[:, 1] > (BOX_HEIGHT-3)]
        draw_points(roi,bottom_edge)
    

        left_edge= max_cont[max_cont[:, 0] < 2]
        # draw_points(roi,left_edge)
        
        right_edge=max_cont[max_cont[:, 0] > (BOX_WIDTH-3)]
        # draw_points(roi,right_edge)

        if bottom_edge.size:        
        
            # if top_edge.size and left_edge.size and right_edge.size:
            #     print("+")
            #     pass
            # elif top_edge.size and left_edge.size:
            #     print("TL")
            #     pass
            # elif top_edge.size and right_edge.size:
            #     print("TR")
            #     pass
            # elif left_edge.size and right_edge.size:
            #     print("T")
            #     pass
            # elif left_edge.size:
            #     print("L")
            #     pass
            # elif right_edge.size:
            #     print("R")
            #     pass
            # else:            
            bottom_edge_mid_point=get_point(bottom_edge,0)
            error=bottom_edge_mid_point[0]-BOX_HALF_WIDTH
            norm_error=error/BOX_HALF_WIDTH
            # print(norm_error)
            cv2.circle(roi,bottom_edge_mid_point,3,(0,255,255),3)
            # TODO : Handle end of the line
            return 1,bin_frame,norm_error



        else:
            # TODO : Handle end of miss the line with checking otsu thresold
            pass

    return 0,bin_frame,0

def pid(error: int) -> None:
    global prev_error
    global acc_error

    correction = KP*error + KI*(acc_error + error) + KD*(error - prev_error)
    acc_error += error
    prev_error = error

    left_motor_velo = AVG_SPEED + correction
    right_motor_velo = AVG_SPEED - correction

    # print("L:",left_motor_velo,"\t, R:",right_motor_velo)

    motor_driver.forward(left_motor_speed=left_motor_velo, right_motor_speed=right_motor_velo)


def test():
    roi,img=get_roi()
    bin_frame,norm_error=process_roi(roi)
    # print(norm_error)
    cv2.imshow('img',img)
    cv2.imshow('roi',roi)
    cv2.imshow('frame',bin_frame)

def follow():
    roi,img=get_roi()
    is_max_cont,bin_frame,norm_error=process_roi(roi)
    if is_max_cont: pid(norm_error)
    # cv2.imshow('img',img)
    # cv2.imshow('roi',roi)
    # cv2.imshow('frame',bin_frame)



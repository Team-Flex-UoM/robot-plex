import cv2
import numpy as np

from plex.camera import Camera

BOX = (440, 250, 320, 240) # (x,y,w,h)

BOX_WIDTH=BOX[2]
BOX_HEIGHT=BOX[3]
BOX_HALF_WIDTH=BOX_WIDTH//2

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
    return max_contour

# def get_intersection(frame: )



def get_point(conts: np.ndarray, _axis: int):    
    return (np.amin(conts,axis=_axis)+np.amax(conts,axis=_axis))//2
    

def process_roi():
    img = cam.get_frame()
    roi = img[BOX[1] - BOX[3]//2: BOX[1] + BOX[3]//2, BOX[0] - BOX[2]//2: BOX[0] + BOX[2]//2, :]
    
    conts = get_line_contour(roi)
    conts = conts.reshape(conts.shape[0], -1)

    left_edge = conts[conts[:, 1] < 2]
    # left_edge_line,left_edge_point=get_point(left_edge,0)

    right_edge=conts[conts[:, 1] > (BOX_WIDTH-3)]
    # right_edge_line,right_edge_point=get_point(right_edge,0)

    top_edge= conts[conts[:, 0] < 2]

    bottom_edge=conts[conts[:, 0] > (BOX_HEIGHT-3)]

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
            bottom_edge_point=get_point(bottom_edge,1)
            error=bottom_edge_point-BOX_HALF_WIDTH
            norm_error=error/BOX_HALF_WIDTH



    else:
        # missed the line
        pass





    if len(arr) > 0:
        cv2.circle(img, arr[0], 2,(255,0,0),3)
    print(img.shape)

    # left edge





def test():
    img = cam.get_frame()
    img = img[BOX[1] - BOX[3]//2: BOX[1] + BOX[3]//2, BOX[0] - BOX[2]//2: BOX[0] + BOX[2]//2, :]
    # contour = get_line_contour(img)
    # con = contour.reshape(contour.shape[0], -1)
    # arr = con[con[:, 1] > 245]
    # if len(arr) > 0:
    #     cv2.circle(img, arr[0], 2,(255,0,0),3)
    # print(img.shape)
    return img

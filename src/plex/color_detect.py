import numpy as np
import cv2

red_lower1=np.array((0,97,28),dtype=np.uint8)
red_upper1=np.array((10,255,255),dtype=np.uint8)

red_lower2=np.array((160,97,28),dtype=np.uint8)
red_upper2=np.array((179,255,255),dtype=np.uint8)

green_lower=np.array((45,97,28),dtype=np.uint8)
green_upper=np.array((80,255,255),dtype=np.uint8)

blue_lower=np.array((96,97,28),dtype=np.uint8)
blue_upper=np.array((131,255,255),dtype=np.uint8)

def to_hsv(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)    

def extract_red(img):
    mask1=cv2.inRange(img,red_lower1,red_upper1)
    mask2=cv2.inRange(img,red_lower2,red_upper2)
    mask=cv2.bitwise_or(mask1,mask2)
    return mask2

def extract_green(img):
    mask=cv2.inRange(img,green_lower,green_upper)
    return mask

def extract_blue(img):
    mask=cv2.inRange(img,blue_lower,blue_upper)
    return mask 

def on_green_patch(roi,pathc_thres):
    roi_hsv=to_hsv(roi)
    green=extract_green(roi_hsv)

    if np.sum(green)>pathc_thres:return True
    return False

    

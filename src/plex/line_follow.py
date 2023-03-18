import cv2
import numpy as np

from plex.camera import Camera

BOX = (440, 250, 320, 240) # (x,y,w,h)

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

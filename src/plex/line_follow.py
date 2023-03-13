import cv2
import numpy as np

from plex.camera import Camera

LINE_BOX = ((100,300),(540,400)) # [(x1, y1), (x2, y2)]

def init(cam_node: Camera) -> None:
    global cam
    cam = cam_node

def get_bin_frame(frame: np.ndarray) -> np.ndarray:
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, bin_frame = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return bin_frame

def get_line_contour(frame: np.ndarray) -> np.ndarray:
    cropped_frame = frame[LINE_BOX[0][1]:LINE_BOX[1][1], LINE_BOX[0][0]:LINE_BOX[1][0], :]
    bin_frame = get_bin_frame(cropped_frame)
    contours, _ = cv2.findContours(bin_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    max_contour = max(contours, key = cv2.contourArea)
    return max_contour

def test():
    img = get_line_contour(cam.get_frame())
    return img

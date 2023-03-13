import cv2
import numpy as np

from plex.camera import Camera

def init(cam_node: Camera) -> None:
    global cam
    cam = cam_node

def get_line_mask() -> np.ndarray:
    gray_frame = cv2.cvtColor(cam.get_frame(), cv2.COLOR_BGR2GRAY)
    ret, bin_frame = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return bin_frame

import cv2
import numpy as np

from plex.camera import Camera
import plex.motor_driver as motor_driver

BOX = (440, 250, 320, 240) # (x,y,w,h)

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
    return max_contour

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

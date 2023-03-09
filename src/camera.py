import cv2
import numpy as np

# Class constants
WIDTH = 640
HEIGHT = 480
_K = np.array([[258.834980287596, 0.0, 315.06271814581396], [0.0, 259.2571348729949, 229.82338632554638], [0.0, 0.0, 1.0]])
_D = np.array([[0.03771034946935066], [-0.06873597576438498], [0.19581964746039696], [-0.2649961510264901]])
_MAP_1, _MAP_2 = cv2.fisheye.initUndistortRectifyMap(_K, _D, np.eye(3), _K, (WIDTH, HEIGHT), cv2.CV_16SC2)

WHITE = (np.array([0,0,100]), np.array([255,35,255]))

class Camera:
	def __init__(self):
		# private
		self._cap = cv2.VideoCapture(0)
		# public
	
	def _get_frame(self) -> np.ndarray:
		ret, frame = self._cap.read()
		assert ret, "There is an error while reading VideoCapture"
		frame = cv2.remap(frame, _MAP_1, _MAP_2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT) # fisheye cleaning
		return frame
	
	def get_mask_frame(self, color):
		hsv_frame = cv2.cvtColor(self._get_frame(), cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(hsv_frame, color[0], color[1])
		return mask
	
	def __del__(self):
		self._cap.release()

if __name__ == "__main__":
    print("Please run the 'main.py' file")
	
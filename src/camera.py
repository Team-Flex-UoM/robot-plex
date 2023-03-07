import cv2
import numpy as np

# fisheye cleaning parameters
DIM = (640, 480)
K = np.array([[258.834980287596, 0.0, 315.06271814581396], [0.0, 259.2571348729949, 229.82338632554638], [0.0, 0.0, 1.0]])
D = np.array([[0.03771034946935066], [-0.06873597576438498], [0.19581964746039696], [-0.2649961510264901]])
MAP_1, MAP_2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)

class Camera:
	def __init__(self):
		# private
		self._cap = cv2.VideoCapture(0)

		# public
		self.WIDTH = DIM[0]
		self.HEIGHT = DIM[1]
	
	def get_frame(self) -> np.ndarray:
		ret, frame = self._cap.read()
		assert ret, "There is an error while reading VideoCapture"

		# undistort fisheye
		frame = cv2.remap(frame, MAP_1, MAP_2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

		return frame
	
	def __del__(self):
		self._cap.release()

if __name__ == "__main__":
    print("Please run the 'main.py' file")
	
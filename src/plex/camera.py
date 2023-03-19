import cv2
import numpy as np
from time import sleep

# Class constants
WIDTH = 640
HEIGHT = 480
_K = np.array([[258.22452392587803, 0.0, 310.227356524318], [0.0, 258.41055987158467, 229.22622290238198], [0.0, 0.0, 1.0]])
_D = np.array([[0.03926573368675932], [-0.012201178250275507], [-0.008355412357037958], [0.0027249791614959665]])
_MAP_1, _MAP_2 = cv2.fisheye.initUndistortRectifyMap(_K, _D, np.eye(3), _K, (WIDTH, HEIGHT), cv2.CV_16SC2)

class Camera:
	def __init__(self):
		# private
		self._cap = cv2.VideoCapture(0)
		# public
	
	def get_frame(self) -> np.ndarray:
		ret, frame = self._cap.read()
		assert ret, "There is an error while reading VideoCapture" # TODO: return blank frame if error occurred
		# frame = cv2.remap(frame, _MAP_1, _MAP_2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT) # fisheye cleaning
		return frame

	def record(self):
		
		i=0
		while(True):
			frame = self.get_frame()
			cv2.imshow('frame', frame)
			cv2.imwrite('imgs/{}.png'.format(i),frame)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
			i+=1
			sleep(1)
			
	
	def __del__(self):
		self._cap.release()

if __name__ == "__main__":
    print("Please run the 'main.py' file")
	
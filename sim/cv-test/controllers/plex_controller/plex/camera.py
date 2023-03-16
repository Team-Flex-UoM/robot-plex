import cv2
import numpy as np
from controller import Robot,Camera,Display

# Class constants
WIDTH = 640
HEIGHT = 480
_K = np.array([[258.22452392587803, 0.0, 310.227356524318], [0.0, 258.41055987158467, 229.22622290238198], [0.0, 0.0, 1.0]])
_D = np.array([[0.03926573368675932], [-0.012201178250275507], [-0.008355412357037958], [0.0027249791614959665]])
_MAP_1, _MAP_2 = cv2.fisheye.initUndistortRectifyMap(_K, _D, np.eye(3), _K, (WIDTH, HEIGHT), cv2.CV_16SC2)

class Camera:
	def __init__(self,robot):
		# private
		timestep = int(robot.getBasicTimeStep())
		self._camera=robot.getDevice("camera")
		self._camera.enable(timestep)
		self.imageWidth=self._camera.getWidth()
		self.imageHeight=self._camera.getHeight()
		self._display=robot.getDevice("display")
		
		# public
	
	def get_frame(self) -> np.ndarray:
		image_in_raw=self._camera.getImage()  
		image_in_list=list(image_in_raw)
		image_in_arr=np.array(image_in_list,dtype=np.uint8)
		image_in_bgra=np.reshape(image_in_arr,(self.imageHeight,self.imageWidth,4)) # image format : BGRA
		# image=np.reshape(image_in_arr,(imageHeight,imageWidth,4)) [:,:,:-1]  # image format : BGR
		image_in_bgr=cv2.cvtColor(image_in_bgra,cv2.COLOR_BGRA2BGR)
		return image_in_bgr

	def show_frame(self,frame):
		image_out_bgr=cv2.cvtColor(frame,cv2.COLOR_BGR2BGRA)
		image_out_arr=image_out_bgr.flatten()
		image_out_list=list(image_out_arr)    
		image_out_raw=bytes(image_out_list)
		ir=self._display.imageNew(image_out_raw,Display.BGRA,self.imageWidth,self.imageHeight)
		self._display.imagePaste(ir,0,0,False)
		self._display.imageDelete(ir)
    
	
	def __del__(self):
		pass

if __name__ == "__main__":
    print("Please run the 'main.py' file")
	
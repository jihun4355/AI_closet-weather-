import cv2
from picamera2 import Picamera2

import time

class Camera:
	def __init__(self):
		self.cam = Picamera2()
		
		config = self.cam.create_video_configuration(main={"size": self.cam.sensor_resolution, "format":"RGB888"})
		
		self.cam.configure(config)

		self.cam.start()
		time.sleep(2)
		self.pt = time.time()
		self.ct = 0
		self.dt = 0
		self.size = (640, 480)
	def update(self):
		self.ct = time.time()
		self.frame= self.cam.capture_array()
		self.frame = cv2.resize(self.frame, self.size)
		self.frame = cv2.flip(self.frame, 1)
		self.dt = self.pt - self.ct
		self.pt = self.ct
	
	def show(self):
		cv2.imshow("stream",self.frame)
 
	def release(self):
		self.cam.stop()
		cv2.destroyAllWindows()
	
	def getFrame(self):
		return self.frame

	def setSize(self, x, y):
		self.size = (x, y)
		
	def getDT(self):
		return self.dt
		
	def imgShow(self, title, img):
		cv2.imshow(title, img)
	
	def __del__(self):
		pass
	

if __name__ == '__main__':
	cam = Camera()
	
	while True:
		cam.update()
		cam.show()
		
		print(cam.getDT())
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	
	cam.release()
	
	
	

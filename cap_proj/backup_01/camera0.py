import cv2
import numpy as np
from picamera2 import Picamera2
import time


cam = Picamera2()


config = cam.create_video_configuration(
	#main={"size": (640, 640), "format": "RG
	main={"size": cam.sensor_resolution, "format":"RGB888"}
#	lores={"size": (int(3280/5), int(2464/5)), "format": "YUV420"}
)

cam.configure(config)


cam.start()
pt = time.time()
while True:
	ct = time.time()
	dt = ct - pt
	pt = ct
	
	print("dt:",dt)
	#frame = cam.capture_array("lores")
	frame = cam.capture_array()
	#frane = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR_I420)
	frame = cv2.resize(frame, (640, 480))
	frame = cv2.flip(frame, 1)
	cv2.imshow('Camera Stream', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
cam.stop()
cv2.destroyAllWindows()

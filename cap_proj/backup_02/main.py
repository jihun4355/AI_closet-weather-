from camera import *
from detect import *
from bunriu import *
import os

camera = Camera()

camera.size = (416, 416)
current_directory = os.getcwd()
onnx_model_path = os.path.join(current_directory, 'clth_md3.onnx')

detector = Detector(onnx_model_path)

clthMgr = ClothesManager()

sorter = ClothesSorter(detector, clthMgr)

while True:
    
    camera.update()
    sorter.update()
    
    
    img = camera.getFrame()
    img = detector.detect(img)
    camera.imgShow("aaaa", img)
    
    
    #print(camera.getDT())
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

camera.release()

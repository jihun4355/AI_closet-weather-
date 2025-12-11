import onnxruntime as ort
import numpy as np
from PIL import Image
import cv2

def preprocess_image(img):
            
            img_resized = np.transpose(img, (2, 0, 1))
            img_resized = img_resized / 255.0
            img_resized = np.expand_dims(img_resized, axis=0).astype(np.float32)
            
            return img_resized

class Detector:
    class_name = []

    def __init__(self, model_path):
        #options = ort.SessionOptions()
        #options.intra_op_num_threads = 2

        self.session = ort.InferenceSession(model_path, providers=['CPUExecutionProvider']) #, sess_options = options)
        Detector.class_name = ['ha', 'outer','sang']
        
        self.mostObj = [0, 0, 0, 0, 0, 0] 
        self.cutObj = None
        
    def detect(self, img):
        self.mostObj = [0, 0, 0, 0, 0, 0]
        self.cutObj = None
        
        
        img_resized = preprocess_image(img)

        session = self.session

        input_name = session.get_inputs()[0].name
        output_name = session.get_outputs()[0].name
        output = session.run([output_name], {input_name: img_resized})
        
        output = np.array(output[0])
        output = np.array(output[0])
        boxes = []
        score = []  #score, class id

        class_idx = []
        for detection in output:
            confidence = detection[4]
            if confidence > 0.7:
                x, y, w, h = detection[:4]
                if h > 250 or w < 10 or h > 250 or h < 10:
                    break

                class_index = np.argmax(detection[5:]) # highest class Extract

                #Most conf Obj
                if self.mostObj[4] < confidence:
                    self.mostObj = [x, y, w, h, confidence, class_index]

        if self.mostObj[0]:
            x, y, w, h, conf, idx = self.mostObj
            print(x, y, w, h, conf, idx)
            x1 = int(x - w / 2)
            y1 = int(y - h / 2)
            x2 = int(x + w / 2)
            y2 = int(y + h / 2)
            
            class_str = Detector.class_name[idx]
            self.mostObj[5] = class_str
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"Class {class_str}: {conf:.2f}   ({int(x)},{int(y)})"
            
            
            cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            self.cutObj = img[x1, y1, x2, y2]
    
            print(self.mostObj[5])
        else:
            print("No Object!!!!!!!!!!!!!!!")
        return img


    def getObject(self):
        return self.mostObj, self.cutObj


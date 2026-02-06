import cv2 as cv
from picamera2 import Picamera2
import time

object_detector = cv.createBackgroundSubtractorMOG2()

picam2 = Picamera2()
config = picam2.create.preview_configuration(main= {"format"="XRGB8888", "size" = (640, 640)})
picam2.configure(config)
picam2.start()

print("picam2 starts, press 'q' to quit.")


try: 
    while True:
        frame = picam2.capture_array()
    
        height, width, _ = frame.shape
    
        #extract region of interest
        
        blurred = cv.GaussianBlur(frame, (7, 7), 0)
        cv.waitKey(50)
        #Object_detection
        mask = object_detector.apply(blurred)
        contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            
            area = cv.contourArea(cnt)
            if area < 5000:
                continue
            
            ##cv.drawContours(frame, [cnt], -1, (0, 255, 0), 2)
            x, y, w, h = cv.boundingRect(cnt)
            cv.rectangle(frame, (x, y), (x+w, y+h), (0,255,0))


finally: 
    picam2.stop()
    cv.destroyAllWindows()
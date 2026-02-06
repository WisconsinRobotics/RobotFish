import cv2

cap = cv2.VideoCapture(0)
object_detector = cv2.createBackgroundSubtractorMOG2()

while True:
    ret, frame = cap.read()
    if not ret:
        break
    height, width, _ = frame.shape
    print(height, width)

    blurred = cv2.GaussianBlur(frame, (3, 3), 0)
    cv2.waitKey(100)
    #Object_detection

    mask = object_detector.apply(blurred)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        
        area = cv2.contourArea(cnt)
        if area < 5000:
            continue
        
        
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0))

    cv2.imshow("usb cam", frame)
    
    if cv2.waitKey(1) == 27: #esl to exit
        break

cap.release()
cv2.destroyAllWindows()
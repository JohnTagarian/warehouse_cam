import cv2
import numpy as np
from PIL import Image 
cap = cv2.VideoCapture(2)

if not cap.isOpened():
    raise IOError("Cannot open webcam")

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 840)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 680)
 
# def check_tone(tone_low,tone_high):
#     pass

while True:
    # Read a frame from the camera
    try:
        ret, frame = cap.read()
        h,w,_ = frame.shape

        cx =int(w/2)
        cy =int(h/2)
        # If the frame was not read correctly, break out of the loop
        if not ret:
            break


        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        pixel_center = hsv_frame[cy, cx]
        print(pixel_center)

        hsv = pixel_center[0],pixel_center[1],pixel_center[2]
        cv2.circle(frame,(cx,cy),5,(0,255,0),3)

        
        # Display the frame
        cv2.imshow('Webcam', frame)

        # Wait for a key press
        key = cv2.waitKey(1)

        # If the 'q' key was pressed, break out of the loop
        if key == ord('q'):
            break
    except:
        print("ex err");

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()


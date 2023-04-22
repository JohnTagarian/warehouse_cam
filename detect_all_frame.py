import cv2
from pyzbar.pyzbar import decode
from PIL import Image
import numpy as np




# Initialize the camera
cap = cv2.VideoCapture(2)

# yellow = [0, 255, 255]  # yellow in BGR colorspace
# blue = [255,0,0]
# color_list = [[0,0,255]]
# detect_tag = ['yellow']
# Check if the camera was initialized correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

# Set the frame size
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)



# Start the video stream
while True:
    # Read a frame from the camera
    detect_color = ''
    qr = ''
    ret, frame = cap.read()

    # If the frame was not read correctly, break out of the loop
    if not ret:
        break

    # Detect QR codes in the frame
    qr_codes = decode(frame)

    # Draw a rectangle around each detected QR code
    for qr_code in qr_codes:
        x, y, w, h = qr_code.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Decode the QR code and print the result
        qr_code_data = qr_code.data.decode('utf-8')
        qr = qr_code_data
        
        



    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lowerLimit_green  = np.array([40,120,100])
    upperLimit_green = np.array([90,250,200])
    mask_green = cv2.inRange(hsvImage, lowerLimit_green, upperLimit_green)
    mask_green_ = Image.fromarray(mask_green)
    bbox_green = mask_green_.getbbox()

    if bbox_green is not None:
        x1, y1, x2, y2 = bbox_green
        detect_color = 'green'
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)       



    lowerLimit_yellow  = np.array([20,100,0])
    upperLimit_yellow = np.array([40,250,255])
    mask_yellow = cv2.inRange(hsvImage, lowerLimit_yellow, upperLimit_yellow)
    mask_yellow_ = Image.fromarray(mask_yellow)
    bbox_yellow = mask_yellow_.getbbox()

    if bbox_yellow is not None:
        x1, y1, x2, y2 = bbox_yellow
        detect_color = 'yellow'
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 5)

    
    lowerLimit_blue  = np.array([90,100,120])
    upperLimit_blue = np.array([120,250,255])
    mask_blue = cv2.inRange(hsvImage, lowerLimit_blue, upperLimit_blue)
    mask_blue_ = Image.fromarray(mask_blue)
    bbox_blue = mask_blue_.getbbox()

    if bbox_blue is not None:
        x1, y1, x2, y2 = bbox_blue
        detect_color = 'blue'
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 5)      

    cv2.imshow('Webcam', frame)
    cv2.imshow('mask_blue', mask_blue)

    print(detect_color,qr)

    # Wait for a key press
    key = cv2.waitKey(1)

    # If the 'q' key was pressed, break out of the loop
    if key == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()

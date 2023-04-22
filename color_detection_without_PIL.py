import cv2
import numpy as np
from pyzbar.pyzbar import decode

# Initialize the camera
cap = cv2.VideoCapture(2)

# Check if the camera was initialized correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

# Set the frame size
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Define the lower and upper bounds of the color to detect
# lower_color_bounds = np.array([40, 150, 50])
# upper_color_bounds = np.array([75, 255, 200])

#                            red                         green                      yellow                  blue
lower_color_bounds = [np.array([0, 100, 80]),np.array([38, 220, 60]),np.array([22, 150, 100]),np.array([100, 50, 150])]
upper_color_bounds = [np.array([10, 255, 255]),np.array([75, 255, 110]),np.array([38, 255, 255]),np.array([130, 255, 220])]
lower_color_bounds_2 = [np.array([160, 100, 80])]
upper_color_bounds_2 = [np.array([179, 255, 255])]
# Start the video stream
while True:
    statea = ''
    stateb = ''
    # Read a frame from the camera
    ret, frame = cap.read()

    # If the frame was not read correctly, break out of the loop
    if not ret:
        break

    # Convert the frame to the HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Detect QR codes in the frame
    qr_codes = decode(frame)

    # Draw a rectangle around each detected QR code
    for qr_code in qr_codes:
        x, y, w, h = qr_code.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Decode the QR code and print the result
        qr_code_data = qr_code.data.decode('utf-8')
        if qr_code_data == '2':
            statea = '2'
            

    # Detect the color in the frame    
    mask1_red = cv2.inRange(hsv_frame, lower_color_bounds[0], upper_color_bounds[0])
    mask2_red = cv2.inRange(hsv_frame, lower_color_bounds_2[0], upper_color_bounds_2[0])
    mask_red = cv2.bitwise_or(mask1_red, mask2_red)

    mask_green = cv2.inRange(hsv_frame, lower_color_bounds[1], upper_color_bounds[1])
    mask_yellow = cv2.inRange(hsv_frame, lower_color_bounds[2], upper_color_bounds[2])
    mask_blue = cv2.inRange(hsv_frame, lower_color_bounds[3], upper_color_bounds[3])
    

    
    
    # Apply a Gaussian blur to the mask
    blurred_mask_red = cv2.GaussianBlur(mask_red, (7, 7), 0)
    blurred_mask_green = cv2.GaussianBlur(mask_green, (7, 7), 0)
    blurred_mask_yellow = cv2.GaussianBlur(mask_yellow, (7, 7), 0)
    blurred_mask_blue = cv2.GaussianBlur(mask_blue, (7, 7), 0)

    # Find contours in the blurred mask
    contours_red, _ = cv2.findContours(blurred_mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(blurred_mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_yellow, _ = cv2.findContours(blurred_mask_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_blue, _ = cv2.findContours(blurred_mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw a rectangle around each detected contour
    for contour in contours_red:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        stateb = 'red'

    for contour in contours_green:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        stateb = 'green'

    for contour in contours_yellow:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
        stateb = 'yellow'
    
    for contour in contours_blue:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        stateb = 'blue'
    

    # Display the frame
    cv2.imshow('Webcam', frame)

    # Wait for a key press
    key = cv2.waitKey(1)

    # If the 'q' key was pressed, break out of the loop
    if key == ord('q'):
        break
    print(stateb,statea)
# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()

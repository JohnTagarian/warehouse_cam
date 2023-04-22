import cv2
from pyzbar.pyzbar import decode

# Initialize the camera
cap = cv2.VideoCapture(2)

# Check if the camera was initialized correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

# Set the frame size
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

tone = {'red1':[[160,0,10],[179,220,256]],'red2':[[0,0,20],[10,220,256]],'yellow':[[20,100,0],[40,250,255]],'green':[[40,10,100],[60,250,255]],'blue':[[90,100,120],[120,250,255]]}
qr =''
# Start the video stream
while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # If the frame was not read correctly, break out of the loop
    if not ret:
        break

    # Detect QR codes in the frame
    qr_codes = decode(frame)

    # Draw a rectangle around each detected QR code
    color ='undefined'
    for qr_code in qr_codes:
        x, y, w, h = qr_code.rect

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        pixel_center = hsv_frame[y, x]
        print(pixel_center)

        hsv = pixel_center[0],pixel_center[1],pixel_center[2]

        
        if ((hsv[0] > tone['red2'][0][0] and hsv[0] < tone['red2'][1][0]) and (hsv[1] > tone['red2'][0][1] and hsv[1] < tone['red2'][1][1]) and (hsv[2] > tone['red2'][0][2] and hsv[2] < tone['red2'][1][2])):
            color = 'red'
        elif (hsv[0] > tone['yellow'][0][0] and hsv[0] < tone['yellow'][1][0]) and (hsv[1] > tone['yellow'][0][1] and hsv[1] < tone['yellow'][1][1]) and (hsv[2] > tone['yellow'][0][2] and hsv[2] < tone['yellow'][1][2]):
            color = 'yelow'
        elif (hsv[0] > tone['green'][0][0] and hsv[0] < tone['green'][1][0]) and (hsv[1] > tone['green'][0][1] and hsv[1] < tone['green'][1][1]) and (hsv[2] > tone['green'][0][2] and hsv[2] < tone['green'][1][2]):
            color = 'green'         
        elif (hsv[0] > tone['blue'][0][0] and hsv[0] < tone['blue'][1][0]) and (hsv[1] > tone['blue'][0][1] and hsv[1] < tone['blue'][1][1]) and (hsv[2] > tone['blue'][0][2] and hsv[2] < tone['blue'][1][2]):
            color = 'blue'            
        cv2.circle(frame,(x-50,y),5,(0,255,0),3)
        

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Decode the QR code and print the result
        qr_code_data = qr_code.data.decode('utf-8')
        qr = qr_code_data
        

    # Display the frame
    cv2.imshow('frame', frame)
    print(color,qr)
    # Wait for a key press
    key = cv2.waitKey(1)

    # If the 'q' key was pressed, break out of the loop
    if key == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()

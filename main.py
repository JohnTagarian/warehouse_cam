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

# Define colors
colors = {
    'red': ((160, 0, 10), (179, 220, 256)),
    'red2': ((0, 0, 20), (40, 45, 100)),
    'yellow': ((80, 160, 0), (105, 250, 255)),
    'green': ((20, 10, 0), (60, 100, 80)),
    'blue': ((90, 10, 0), (120, 100, 55))
}

qr = ''
# Start the video stream
while True:
    # Read a frame from the camera
    color = None
    ret, frame = cap.read()

    # If the frame was not read correctly, break out of the loop
    if not ret:
        break

    # Detect QR codes in the frame
    qr_codes = decode(frame)

    # Loop over each detected QR code
    for qr_code in qr_codes:
        x, y, w, h = qr_code.rect

        # Get the center pixel of the QR code
        
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        pixel_center = frame[y, x-50]
        print(pixel_center)
        hsv = pixel_center[0],pixel_center[1],pixel_center[2]
        

        # Determine the color of the center pixel
        
        for c, r in colors.items():
            if r[0][0] <= hsv[0] <= r[1][0] and r[0][1] <= hsv[1] <= r[1][1] and r[0][2] <= hsv[2] <= r[1][2]:
                color = c
                break

        # Draw a circle at the center pixel and a rectangle around the QR code
        # if color is not None:
        cv2.circle(frame, (x-50, y), 5, (0, 255, 0), 3)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Decode the QR code and print the result
        qr_code_data = qr_code.data.decode('utf-8')
        qr = qr_code_data

    # Display the frame
    cv2.imshow('frame', frame)
    print(qr,color)

    # Wait for a key press
    if cv2.waitKey(1) == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()

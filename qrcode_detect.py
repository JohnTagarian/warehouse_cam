import cv2
from pyzbar.pyzbar import decode

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise IOError("Cannot open webcam")

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)




while 1:
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
        print(qr_code_data)    

    cv2.imshow("Output", frame)
    if cv2.waitKey(1) == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
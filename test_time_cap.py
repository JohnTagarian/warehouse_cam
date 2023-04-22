import cv2
import time


# Opens the inbuilt camera of laptop to capture video.
webCam = cv2.VideoCapture(2)
currentframe = 0
time_st = time.time()
pre_time = 0
while (True):
    success, frame = webCam.read()
    
    T = time.time() - time_st 
    if  T - pre_time> 0.5:
    # Save Frame by Frame into disk using imwrite method
        cv2.imwrite('frame2.jpg', frame)
        pre_time = T
        print('w')
    cv2.imshow("Output", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    


webCam.release()
cv2.destroyAllWindows()

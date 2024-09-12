#ou can use OpenCV to record video from your USB camera. Here is a simple Python script that uses OpenCV to capture video from a USB camera and display it

import cv2

testVid_path= '/home/koogleblitz/DragonVision-RoboSubCV/robosubGateCmpl.mp4'
cap = cv2.VideoCapture(testVid_path)



while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:


        # Display the resulting frame
        cv2.imshow('frame', frame)

        # Quit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        print("[x:] ERROR: no frames read")
        break

# Release everything when done
cap.release()
cv2.destroyAllWindows()

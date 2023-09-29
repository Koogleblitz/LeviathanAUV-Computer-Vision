# [+:] You can use OpenCV to record video from your USB camera. 
    # Here is a simple Python script that uses OpenCV to capture video from a USB camera and (supposed to) save it to a file
    # But having issues recording, so i'm going to save each frame individually as a pic

import cv2
import os

if not os.path.exists('frames'): 
    os.makedirs('frames')


# Create a VideoCapture object
cap = cv2.VideoCapture(1)

# Define the codec and create a VideoWriter object if recording
#recorder = cv2.VideoWriter_fourcc(*'mp4v')
#out = cv2.VideoWriter('output3.mp4', recorder, 20.0, (640, 480))

frameLim= 1000


#while(cap.isOpened()):
i=0
while(i<=frameLim):
    ret, frame = cap.read()
    if ret == True:
        # Write the frame into the file 'output.avi' (not working curently)
        # out.write(frame)

        #[+] Hotfix: save each frame individually
        cv2.imwrite(f'frames/frame_{i}.png', frame)
        i+=1 

        # Display the resulting frame
        cv2.imshow('frame_{i}', frame)

 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        print("[x:] ERROR: No frames read. ")
        break

# Release everything when done
cap.release()
#out.release()
cv2.destroyAllWindows()

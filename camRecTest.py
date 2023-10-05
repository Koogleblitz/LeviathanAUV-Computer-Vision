# [+:] You can use OpenCV to record video from your USB camera. 
    # Here is a simple Python script that uses OpenCV to capture video from a USB camera and (supposed to) save it to a file
    # But having issues recording, so i'm going to save each frame individually as a pic

import cv2
import os
import numpy as  np
import shutil
from datetime import datetime

if not os.path.exists('frames'): 
    os.makedirs('frames')
if not os.path.exists('recordings'): 
    os.makedirs('recordings')




#cap = cv2.VideoCapture(2)
# Define the codec and create a VideoWriter object if recording
#recorder = cv2.VideoWriter_fourcc(*'mp4v')
#out = cv2.VideoWriter('output3.mp4', recorder, 20.0, (640, 480))

recording_path= r'C:\Users\richa\OneDrive\CSEC_Robosub\richardCode\Repo\recordings'
vid_Path= r"C:\Users\richa\OneDrive - email.ucr.edu\CSEC_Robosub\richardCode\Repo\recordings\\"
frame_Path=  r"C:\Users\richa\OneDrive - email.ucr.edu\CSEC_Robosub\richardCode\Repo\frames"
dateTime= datetime.now().strftime("%Y%m%d_%H%M%S")

#[+] at frameDiv=2 and frmLim=200, it records at 16-20 fps for ~10 seconds. 
    # Oddly, the png frames yield a smaller file size than the jpg frames. I see no reason to use the jpg frames. 
    # A 10s vid would be ~500kb for jpg and ~400kb for png. 
frmLim= 4500
frmDiv= 2
frmSize= (480,640)
fps= 18
imgType= ".png"



def record_vid():
    print('    --> recording fps: ', fps)
    print('    --> recording imgType: ', imgType)
    print('\n')

    i=0
    #while(cap.isOpened()):
    cap = cv2.VideoCapture(2)
    while(i<=frmLim*frmDiv):
        ret, frame = cap.read()
        if ret == True:
            # Write the frame into the file 'output.avi' (not working curently)
            # out.write(frame)
            #[+] Hotfix: save each frame individually
            if i%frmDiv==0: cv2.imwrite(f'frames/frame_{i//frmDiv}'+imgType, frame)
            i+=1 

            # Display the resulting frame
            cv2.putText(frame, '[::'+str(i)+']', org=(10, 20), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=.5, color= (100,100,255), thickness=2)
            cv2.imshow('frame_', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'): break
        else:
            print("[x:] ERROR: No camera frames read. ")
            break
    cap.release()
    cv2.destroyAllWindows()

def compile_vid(image_folder, video_name, fps=18, imgType= ".png"):
    print('dateTime: ', dateTime)
    print('    --> image_folder: ', image_folder)
    print('    --> compiled fps: ', fps)
    print('    --> compiled imgType: ', imgType, '\n')

    images = [img for img in os.listdir(image_folder) if img.endswith(imgType)]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape
    video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width,height))

    frameCnt= len(images)
    for i, image in enumerate(images):
        video.write(cv2.imread(os.path.join(image_folder, image)))
        if (i%10)==0 or i==frameCnt: print("Compiled: --> ", i, " / ", frameCnt)

    # cv2.destroyAllWindows()
    video.release()


def del_frames():
    print('   --> Deleting frames in ', frame_Path)
    for filename in os.listdir(frame_Path):
        file_path = os.path.join(frame_Path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')


# [+] record video
record_vid()
# [+] Compile Video
compile_vid(image_folder= frame_Path, 
                video_name= vid_Path+dateTime+imgType+".mp4", 
                fps=fps, 
                imgType= imgType)
del_frames()
cv2.destroyAllWindows()

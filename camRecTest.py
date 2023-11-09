# [+:] You can use OpenCV to record video from your USB camera. 
    # Here is a simple Python script that uses OpenCV to capture video from a USB camera and (supposed to) save it to a file
    # But having issues recording, so i'm going to save each frame individually as a pic
        # - Fixed: see below

import cv2
import sys
import os
import numpy as  np
import shutil
from datetime import datetime
window_title = "USB Camera"


if not os.path.exists('frames'): 
    os.makedirs('frames')
if not os.path.exists('recordings'): 
    os.makedirs('recordings')
dateTime= datetime.now().strftime("%Y%m%d_%H%M%S")


#[+] My windows directories -------------------------------------------------------------------
#recording_path= r'C:\Users\richa\OneDrive\CSEC_Robosub\richardCode\Repo\recordings'
#vid_Path= r"C:\Users\richa\OneDrive - email.ucr.edu\CSEC_Robosub\richardCode\Repo\recordings\\"
#frame_Path=  r"C:\Users\richa\OneDrive - email.ucr.edu\CSEC_Robosub\richardCode\Repo\frames"

# [+] My Linux Directories ------------------------------------------------------------------
recording_path= r'./recordings'
vid_Path= r"./recordings/"
frame_Path=  r"./frames"


# [+] gstreamer pipelines - assign addreses to devices here --------------------------------------------|
    #[+] with v4ls utils installed, the command 'v4l2-ctl --list-devices' returns all cameras
pipeline = " ! ".join(["v4l2src device=/dev/video1",
                       "video/x-raw, width=640, height=480, framerate=30/1",
                       "videoconvert",
                       "video/x-raw, format=(string)BGR",
                       "appsink"
                       ])

# Sample pipeline for H.264 video, tested on Logitech C920
h264_pipeline = " ! ".join(["v4l2src device=/dev/video0",
                            "video/x-h264, width=1280, height=720, framerate=30/1, format=H264",
                            "avdec_h264",
                            "videoconvert",
                            "video/x-raw, format=(string)BGR",
                            "appsink sync=false"
                            ])



#[+] at frameDiv=2 and frmLim=200, using frame-byframe method records at 16-20 fps for ~10 seconds. 
    # Oddly, the png frames yield a smaller file size than the jpg frames. I see no reason to use the jpg frames. 
    # A 10s vid would be ~500kb for jpg and ~400kb for png. 
    # On the TX1, using the default black carrier board, with the cam plugged into the OTG socket, the camNum==2OTG, still need to test using the orbitty and using the usb hub
frmLim= 100
frmDiv= 2
frmSize= (480,640)
fps= 18
imgType= ".png"
camNum= 1
camId= "/dev/video1"

# [+] A choice of three modes of capture: regular, v4l2, or gstreamer, with gstreamer also having the additional h264 pipeline option
#cap = cv2.VideoCapture(camNum)
#cap = cv2.VideoCapture(camId, cv2.CAP_V4L2)
cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)

def record_vid():
    print('    --> recording fps: ', fps)
    print('    --> recording imgType: ', imgType)
    print('\n')
    if cap.isOpened()==False: print('\n [x] ERROR: video capture is not opened \n')
    
    
    # [x] (broken) Define the codec and create a VideoWriter object if recording
    #recorder = cv2.VideoWriter_fourcc(*'mp4v')
    #out = cv2.VideoWriter('output.mp4', recorder, 20.0, (640,480))
    # [++] FIX: Video recording is possible using gstreamer pipeline 1 after installing canberra, and using the MFPG format for the videowriter
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    outPath= vid_Path+dateTime+".mp4"
    out = cv2.VideoWriter(outPath, fourcc, 20.0, (640,480))

    i=0
    #while(cap.isOpened()):
    while(i<=frmLim*frmDiv):
        ret, frame = cap.read()
        if ret == True:

            # Write the frame into the file 'output.avi' (not working curently)
            out.write(frame)

            #[+] (deprecated) Hotfix: save each frame individually
            #if i%frmDiv==0: cv2.imwrite(f'frames/frame_{i//frmDiv}'+imgType, frame)
            i+=1
             
            # Display the resulting frame
            cv2.putText(frame, '[::'+str(i)+']', org=(10, 20), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=.5, color= (100,100,255), thickness=2)
            cv2.imshow('frame_', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'): break
            
        else:
            print("    \n--> [x:] ERROR: No camera frames read. \n")
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
    video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), 18, (width,height))

    frameCnt= len(images)
    for i, image in enumerate(images):
        if (i%20)==0 or i==frameCnt: print("Compiled: --> ", i, " / ", frameCnt)
        video.write(cv2.imread(os.path.join(image_folder, image)))
        
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


record_vid()
#compile_vid(image_folder= frame_Path, 
               # video_name= vid_Path+dateTime+imgType+".mp4", 
               # fps=fps, 
               # imgType= imgType)
del_frames()
cv2.destroyAllWindows()

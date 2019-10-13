import cv2
import time

def FrameCapture(path): 
    # Path to video file 
    vidObj = cv2.VideoCapture(path) 
  
    # Used as counter variable 
    count = 0
  
    # checks whether frames were extracted 
    success = 1
  
    while success: 
        vidObj.set(cv2.CAP_PROP_FPS, 25)   # added this line 
        # vidObj object calls read 
        # function extract frames 
        success, image = vidObj.read() 
  
        # Saves the frames with frame-count 
        cv2.imwrite("frames/%d.jpg" % count, image)
  
        count += 1

    return None
import pyautogui 
import cv2 
import numpy as np
import datetime
from time import sleep


def record(filename = "Recording.avi", codec = cv2.VideoWriter_fourcc(*"XVID"), resolution = (1920,1080), fps = 30.0, window = False):
    start = datetime.datetime.now()
    out = cv2.VideoWriter(filename, codec, fps, resolution)
    if window:
        cv2.namedWindow("Live", cv2.WINDOW_NORMAL) 
        cv2.resizeWindow("Live", 480, 270)
    while True:
        img = pyautogui.screenshot() 
        frame = np.array(img) 
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
        out.write(frame)
        if window:
            cv2.imshow('Live', frame)
	    # Stop recording when we press 'q' 
        if cv2.waitKey(1) == ord("q"):
            break
    out.release()  
    cv2.destroyAllWindows()
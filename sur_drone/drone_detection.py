from threading import Thread
from time import sleep
import cv2
import numpy as np

class Detector(Thread):



    def __init__(self, queue, video_queue):
        super(Detector, self).__init__()
        self.queue = queue
        self.video_queue = video_queue
        self.running = True
        self.n = 0
        self.cap = cv2.VideoCapture(-1)

    def run(self):
        while self.running:
            sleep(0.5)
            #print("Frame %d"%(self.n))
            self.n += 1
            if(self.check_detect()):
                self.queue.put("DETECT") #48.4188, -4.4723


    def check_detect(self):
        # Take each frame
        _, frame = self.cap.read()
        
        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
        # define range of blue color in HSV
        lower_orange = np.array([0,100,100])
        upper_orange = np.array([5,255,255])

        # Threshold the HSV image to get only orange colors
        mask = cv2.inRange(hsv, lower_orange, upper_orange)

        (_,cnts, _) = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        # Find the index of the largest contour
        areas = [cv2.contourArea(c) for c in cnts]
        if len(areas) != 0:
            max_index = np.argmax(areas)
            cnt=cnts[max_index]
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

        self.video_queue.put(frame)
        #cv2.imshow('video', frame)
        #cv2.waitKey(1)

        if len(areas) != 0:
            return True

        return False



import cv2 as cv
import numpy as np
import HandDectectionModule as htm
import time
import pyautogui

print('running')

#############################
wcam, hcam = 640, 480
wscreen, hscreen = pyautogui.size()
# print (wscreen,hscreen)
frameBdr = 100 #Frame Boundary
smoothening = 5

#############################
cap = cv.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)

#############################

ctime,ptime = 0,0
plocx, plocy = 0,0
clocx, clocy = 0,0

#############################

detector = htm.handDetector(maxHands=1)

while True:
    #1) Finding Landmarks
    success, img = cap.read()
    img = detector.findHands(img,draw=True)
    lmlist = detector.findPosition(img,draw=False)

    #2) Getting tips of Index and Middle finger
    if len(lmlist) != 0 :
        x1,y1 = lmlist[8][1:]
        x2,y2 = lmlist[12][1:]

        #3) Check which finger are up
        fingers = detector.fingersUP()

        ##setting a region for mouse operation
        cv.rectangle(img,(frameBdr,frameBdr),(wcam-frameBdr,hcam-frameBdr),
                     (255,0,255,),2)

        #4) Only Index finger == Moving Mode
        if fingers[1] == 1 and fingers[2] == 0 :

            #5) Coordinate conversion for Mouse operation
            ##setting a region for mouse operation

            x3 = np.interp(x1,(frameBdr,wcam-frameBdr),(0,wscreen))
            y3 = np.interp(y1,(frameBdr,hcam-frameBdr),(0,hscreen))

            #6) Smoothen values
            clocx = plocx + (x3 - plocx)/smoothening
            clocy = plocy + (y3 - plocy)/smoothening
            plocx,plocy = clocx,clocy

            #7) Move Mouse
            pyautogui.moveTo(int(wscreen-clocx),int(clocy),duration=0.001)
            # autopy.mouse.move(wscreen - clocx, clocy)
            cv.circle(img,(x1,y1),15,(255,0,255),-1)


        #8) When both fingers are Up == Clicking mode
        if fingers[1] == 1 and fingers[2] == 1:
            length, img, lineinfo =  detector.findDistance(8,12,img)
            # print(length)

            if length < 25:
                cv.circle(img,(lineinfo[4],lineinfo[5]),
                               10,(0,255,0),-1)
                pyautogui.click()

        # For Scrolling you have to make a YO! sign
        if fingers[1] == 1 and fingers[4] == 1: #DownScroll
            pyautogui.scroll(-200)
        if fingers[1] != 1 and fingers[4] == 1 : # Upscroll (only pinky finger raised)
            pyautogui.scroll(200)


        # Frame Rate
        ctime = time.time()
        fps = 1/(ctime-ptime)
        ptime = ctime
        cv.putText(img, 'FPS: ' + str(int(fps)), (10, 50),cv.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

        #12) Display
        cv.imshow('image',img)
        cv.waitKey(1)




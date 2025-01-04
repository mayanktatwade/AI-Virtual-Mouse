import cv2 as cv
import mediapipe as mp



class handDetector():

    def __init__(self,mode = False, maxHands = 2, complexity = 1,detectionCon =0.5, trackCon =0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.complexity = complexity

        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands(self.mode, self.maxHands,self.complexity,
                                        self.detectionCon,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4,8,12,16,20]

    #Draws Hand Landmarks
    def findHands(self, img, draw=True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)  # mediapipe processes RGB image
        self.results = self.hands.process(imgRGB)

        # Provides position of all the points of hands and draws it
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, handLms, self.mphands.HAND_CONNECTIONS)

        return img

    #Returns Location of every Hand Landmarks
    def findPosition(self, img, handNo=0, draw=True):
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv.circle(img, (cx, cy), 15, (255, 0, 255), cv.FILLED)
        return self.lmList

    #To find whether a finger is Up or Not
    def fingersUP(self):
        fingers = []

        # For thumb
        if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        #For fingers
        for id in range(1,5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

    #Returns the distance between two positions and draws a connecting line
    def findDistance(self,p1,p2,img,draw=True,r=15,t=3):
        x1,y1 = self.lmList[p1][1:]
        x2,y2 = self.lmList[p2][1:]
        cx,cy = (x1+x2)//2 , (y1+y2)//2

        if draw:
            cv.circle(img, (x1, y1), r, (255, 0, 255), -1)
            cv.circle(img, (x2, y2), r, (255, 0, 255), -1)
            cv.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv.circle(img, (cx, cy), r, (0, 0, 255), -1)
        length = ((x2-x1)**2+(y2-y1)**2)**0.5

        return length, img, [x1,y1,x2,y2,cx,cy]















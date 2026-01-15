import cv2
import mediapipe as mp
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


Wcam, Hcam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, Wcam)
cap.set(4, Hcam)
pTime = 0


detector = htm.HandDetector(detectionCon=0.75)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]







while True:
    success , image = cap.read()
    image = detector.findHands(image)
    lmList = detector.findPosition(image, draw=False)
    if len(lmList) != 0:
        # print(lmList[4], lmList[8])
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        cv2.circle(image, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(image, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(image, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(image, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)


        # Hand range 50 - 300
        # Volume Range -65 - 0

        vol = np.interp(length, [50, 300], [minVol, maxVol])
        print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)


        if length < 50:
            cv2.circle(image, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

        cv2.rectangle(image, (50, 150), (85, 400), (0, 255, 0), 3)
        volBar = np.interp(length, [50, 300], [400, 150])
        cv2.rectangle(image, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
        volPer = np.interp(length, [50, 300], [0, 100])
        cv2.putText(image, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)




    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime




    cv2.putText(image , f"FPS: {int(fps)}",(40,50), cv2.FONT_HERSHEY_PLAIN,2 ,(255,0,0),3)


    cv2.imshow("Image", image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
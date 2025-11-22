import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# ============================== SETTINGS ==============================
wCam, hCam = 640, 480
cameraIndex = 0  # Change to 0 if your webcam does not open
smoothness = 10  # Smoother volume transitions (e.g. 10 = snap to nearest 10%)

# ============================== SETUP ==============================
cap = cv2.VideoCapture(cameraIndex)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7, maxHands=1)

# Pycaw setup for system volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

# Initial volume values
vol = 0
volBar = 400
volPer = 0
area = 0
colorVol = (255, 0, 0)

# ============================== MAIN LOOP ==============================
while True:
    success, img = cap.read()
    if not success:
        continue

    # Detect hand and landmarks
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, draw=True)

    if len(lmList) != 0:

        # Calculate bounding box area to determine hand proximity
        area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) // 100

        # Filter only usable hand sizes (distance from camera)
        if 250 < area < 1000:

            # Find distance between thumb (id=4) and index finger (id=8)
            length, img, lineInfo = detector.findDistance(4, 8, img)

            # Convert hand distance to volume % and bar level
            volBar = np.interp(length, [50, 200], [400, 150])
            volPer = np.interp(length, [50, 200], [0, 100])
            volPer = smoothness * round(volPer / smoothness)  # smooth volume percentage

            # Check fingers status (for pinky control)
            fingers = detector.fingersUp()

            # Only set volume when pinky is down
            if not fingers[4]:
                volume.SetMasterVolumeLevelScalar(volPer / 100, None)
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                colorVol = (0, 255, 0)
            else:
                colorVol = (255, 0, 0)

    # ============================== DRAW UI ==============================

    # Volume bar and percentage text
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    # Current volume value display
    cVol = int(volume.GetMasterVolumeLevelScalar() * 100)
    cv2.putText(img, f'Vol Set: {cVol}', (400, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, colorVol, 3)

    # Frame rate display
    cTime = time.time()
    fps = 1 / (cTime - pTime) if cTime != pTime else 0
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    # Show image
    cv2.imshow("Gesture Volume Control", img)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ============================== CLEANUP ==============================
cap.release()
cv2.destroyAllWindows()

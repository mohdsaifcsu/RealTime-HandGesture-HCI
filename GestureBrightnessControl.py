import cv2
import time
import numpy as np
import HandTrackingModule as htm
import wmi

# ============================== SETTINGS ==============================
wCam, hCam = 640, 480
cameraIndex = 0  # Use 1 if you use external webcam
smoothness = 10  # Snap brightness to nearest 10%

# ============================== SETUP ==============================
cap = cv2.VideoCapture(cameraIndex)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7, maxHands=1)

# Windows brightness controller setup
wmi_interface = wmi.WMI(namespace='wmi')
brightness_methods = wmi_interface.WmiMonitorBrightnessMethods()[0]

# Initial values
brightnessBar = 400
brightnessPer = 0
area = 0
colorB = (255, 0, 0)

# ============================== MAIN LOOP ==============================
while True:
    success, img = cap.read()
    if not success:
        continue

    # Detect hand and landmarks
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, draw=True)

    if len(lmList) != 0:
        # Calculate hand size to avoid false triggers
        area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) // 100

        if 250 < area < 1000:
            # Get distance between thumb (4) and index (8)
            length, img, lineInfo = detector.findDistance(4, 8, img)

            # Convert distance to brightness % and bar height
            brightnessBar = np.interp(length, [50, 200], [400, 150])
            brightnessPer = np.interp(length, [50, 200], [0, 100])
            brightnessPer = smoothness * round(brightnessPer / smoothness)

            # Get finger status (check pinky)
            fingers = detector.fingersUp()

            if not fingers[4]:  # Only apply brightness when pinky is down
                brightness_methods.WmiSetBrightness(int(brightnessPer), 0)
                if lineInfo and len(lineInfo) >= 6:
                    cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                colorB = (0, 255, 0)
            else:
                colorB = (255, 0, 0)

    # ============================== DRAW UI ==============================

    # Brightness bar and %
    cv2.rectangle(img, (50, 150), (85, 400), (255, 255, 0), 3)
    cv2.rectangle(img, (50, int(brightnessBar)), (85, 400), (255, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(brightnessPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 255, 0), 3)

    # Brightness value text
    cv2.putText(img, f'Brightness: {int(brightnessPer)}', (350, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, colorB, 3)

    # FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime) if cTime != pTime else 0
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 255), 3)

    # Show output
    cv2.imshow("Gesture Brightness Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ============================== CLEANUP ==============================
cap.release()
cv2.destroyAllWindows()

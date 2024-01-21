# script per testare varie ed eventuali (vuoto al momento)

import cv2
import random
from cvzone.HandTrackingModule import HandDetector



cap = cv2.VideoCapture(0)

while True:
    cv2.imshow("Image", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
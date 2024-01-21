# tutorial drago and drop: https://www.youtube.com/watch?v=6DxN8G9vB50
# programma principale:
# ToDo:
#   funzione divisione (già semi impostata, spero)
#   meccanismo di controllo fine gioco (puzzle corretto)

import cv2
import random
from cvzone.HandTrackingModule import HandDetector


# funzione non attiva
def div(img, backgroud):
    lista_img = []
    W_SIZE, H_SIZE = 3, 3
    height, width, channels = img.shape
    for ih in range(W_SIZE):
        for iw in range(H_SIZE):
            #rand_x = random.randint(0, backgroud.shape[0]-width)
            #rand_y = random.randint(0, backgroud.shape[1]-height)
            x = width/W_SIZE * iw
            y = height/H_SIZE * ih
            h = (height / H_SIZE)
            w = (width / W_SIZE)
            new_img = img[int(y):int(y+h), int(x):int(x+w)]
            lista_img.append(new_img)
            


cap = cv2.VideoCapture(0)
colorR = (255, 0, 255)
cap.set(3, 1280)
cap.set(4, 740)
detector = HandDetector(detectionCon=0.8)

cx, cy, w, h = 100, 100, 200, 200

#im = cv2.imread('img/Lenna.png')
while True:
    succes, img = cap.read()
    image = cv2.flip(img, 1)
    hands, image = detector.findHands(image)
    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"] # list of landmarks (21) points
        l, _, _ = detector.findDistance(lmList1[8], lmList1[12], image)
        if l<30:
            cursur = lmList1[8]
            if cx-w//2 < cursur[0] < cx+w//2 and cy-h//2 < cursur[1] < cy+h//2:
                colorR = 0, 255, 0
                cx = cursur[0]
                cy = cursur[1]
            else: 
                colorR = (255, 0, 255)

    cv2.rectangle(image, (cx-w//2, cy-h//2), (cx+w//2, cy+h//2), colorR, cv2.FILLED)
    #im = cv2.imread('img/Lenna.png')
    #im = cv2.resize(im, ((w, h)))
    #image[cy - h//2: cy+h//2, cx - w//2: cx + w//2] = im



    cv2.imshow("Image", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
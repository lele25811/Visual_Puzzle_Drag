# Script che prende in input un img (Lenna.png),
# la divide in 9 parti uguali e le distribuisce randomicamente 
# su un altra img usata come sfondo.
# prendere spunto per il programma principale

import cv2
import numpy as np
import random
#import cvzone

def div(img, backgroud):
    W_SIZE, H_SIZE = 3, 3
    height, width, channels = img.shape
    for ih in range(W_SIZE):
        for iw in range(H_SIZE):
            rand_x = random.randint(0, backgroud.shape[0]-width)
            rand_y = random.randint(0, backgroud.shape[1]-height)
            x = width/W_SIZE * iw
            y = height/H_SIZE * ih
            h = (height / H_SIZE)
            w = (width / W_SIZE )
            new_img = img[int(y):int(y+h), int(x):int(x+w)]
            x +=rand_x
            y +=rand_y
            backgroud[int(y):int(y+h), int(x):int(x+w)] = new_img



#sfondo = cv2.imread('img/Sfondo.png', cv2.IMREAD_COLOR)
sfondo = cv2.imread('img/sfondo1.png', cv2.IMREAD_COLOR)
img = cv2.imread('img/Lenna.png', cv2.IMREAD_COLOR)
sfondo = cv2.resize(sfondo, (500,500))
img = cv2.resize(img, (100,100))

div(img, sfondo)

cv2.imshow('img', sfondo)
cv2.waitKey(0)

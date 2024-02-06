''' import cv2
import time
from cvzone.HandTrackingModule import HandDetector
import cvzone
import random

cap = cv2.VideoCapture(0)   # Number of the camera
cap.set(3, 1280)            # 3 stands for CAP_PROP_FRAME_WIDTH
cap.set(4, 720)             # 4 stands for CAP_PROP_FRAME_HEIGHT
widthCAP = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
heightCAP = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

detector = HandDetector(detectionCon=0.65)  # The value 0.65 represents the minimum confidence level required for the hand detection algorithm to consider a detected region as a hand.

class DragImg():
    def __init__(self, path, posOrigin):
        self.path = path
        self.posOrigin = posOrigin
     
        self.img = cv2.imread(self.path)

        self.size = self.img.shape[:2]
        
    def update(self, cursor):
        ox, oy = self.posOrigin
        h, w = self.size
        # Check if in region of the image
        if ox < cursor[0] < ox+w and oy < cursor[1] < oy+h:     # cursor[0] gives us x and cursor[1] gives ue y
            self.posOrigin = cursor[0] - w//2, cursor[1] - h//2

def good_pos(used_pos, rand_w, rand_h, w, h):
    for pos in used_pos:
        if ((pos[0] + int(w) < rand_w) or (pos[0] - int(w) > rand_w)) and ((pos[1] + int(h) < rand_h) or (pos[1] - int(h) > rand_h)):
            return True
    return False

img = cv2.imread('img/sfondo1.png')
img2 = img
imgSplit = []
height, width, channels = img.shape
# Number of pieces Horizontally 
W_SIZE  = 3 
# Number of pieces Vertically to each Horizontal  
H_SIZE = 3

used_positions = [] 
# Loop over rows in the grid
for ih in range(H_SIZE):
    # Loop over columns in the grid
    for iw in range(W_SIZE):
        # Calculate the x-coordinate of the top-left corner of the image block
        x = width / W_SIZE * iw 
        # Calculate the y-coordinate of the top-left corner of the image block
        y = height / H_SIZE * ih
        # Calculate the height of each image block based on the grid
        h = height / H_SIZE
        # Calculate the width of each image block based on the grid
        w = width / W_SIZE

        # Extract the image block based on current grid position
        img = img[int(y):int(y+h), int(x):int(x+w)]
        # Generate a unique name for the image block using the current timestamp
        NAME = str(time.time()) 
        # Save the image block to a file in the 'img/' directory
        cv2.imwrite("img/" + str(ih) + str(iw) + ".png", img)
        # Construct the path to the saved image block
        pathImg = "img/" + str(ih) + str(iw) + ".png" 
        rand_w = random.randint(0, widthCAP - int(w))
        rand_h = random.randint(0, heightCAP - int(h))
    
        # Create a DragImg object for the current image block and add it to imgSplit
        imgSplit.append(DragImg(pathImg, [rand_w, rand_h])) 
        # Reset img to the original image for the next iteration
        img = img2

while True:
    success, img = cap.read()   # cap.read() reads a frame from the camera, and success indicates whether the frame was successfully read. img contains the image data.
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)
    
    if hands:       # hands represent a list of hand
        lmList = hands[0]['lmList']    # find the first hand and get the landmarks(the list of the points)
        # Check if clicked
        length, info, img = detector.findDistance(lmList[8][:2], lmList[12][:2], img)    # # lmList[8] is the tip of the index finger, lmList[12] is the tip of the middle finger
        
        if length < 50:
            cursor = lmList[8]
            for imgObject in imgSplit:
                imgObject.update(cursor)
    
     
    for imgObject in imgSplit:
        # Draw images  
        h, w = map(int, imgObject.size)   # shape shows the height, wi  dth and channels of the image
        ox, oy = imgObject.posOrigin
        img[oy:oy+h, ox:ox+w] = imgObject.img    # Put the image at this position

    cv2.imshow("Image", img)    # displays the image in a window with the title "Image".
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break 
        
cap.release()
cv2.destroyAllWindows()  '''

import cv2
import time
from cvzone.HandTrackingModule import HandDetector
import cvzone
import random
import math
import numpy as np

# Set up the video capture
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Get the width and height of the video capture
widthCAP = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
heightCAP = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Initialize the hand detector from the cvzone library
detector = HandDetector(detectionCon=0.65)

# Class to represent draggable images
class DragImg():
    def __init__(self, path, posOrigin):
        self.path = path
        self.posOrigin = posOrigin
        self.img = cv2.imread(self.path)
        self.size = self.img.shape[:2]

    def update(self, cursor):
        ox, oy = self.posOrigin
        h, w = self.size
        # Check if in the region of the image
        if ox < cursor[0] < ox+w and oy < cursor[1] < oy+h:
            self.posOrigin = cursor[0] - w//2, cursor[1] - h//2

# Function to check if a random position is good and has enough distance from used positions
def good_pos(used_pos, rand_w, rand_h, min_distance=230):
    for pos in used_pos:
        distance = math.sqrt((pos[0] - rand_w)**2 + (pos[1] - rand_h)**2)
        if distance < min_distance:
            return False
    return True

# Load an image and create a draggable object for it
img = cv2.imread('img/lenna.png')
img2 = img

height, width, channels = img.shape

# Specify the number of vertical and horizontal splits for the image
W_SIZE = 3
H_SIZE = 3
imgSplit = []
used_positions = []  # List to store used coordinates
rectangle = np.zeros((height, width, 3), dtype=np.uint8)
''' color = (0, 0, 0) 
rectangle[:, :] = color '''

# Draw vertical lines
for i in range(1, W_SIZE):
    x = int((width / W_SIZE) * i)
    cv2.line(rectangle, (x, 0), (x, height), (255, 255, 255), 2) # (x, 0) is the starting point of the line (top of the image)
                                                                 # (x, height) is the ending point of the line (bottom of the image)
                                                                 # (255, 255, 255) is the color of the line
                                                                 # 2 is the thickness of the line
# Draw horizontal lines
for j in range(1, H_SIZE):
    y = int((height / H_SIZE) * j)
    cv2.line(rectangle, (0, y), (width, y), (255, 255, 255), 2) # (0, y) is the starting point of the line (leftmost side)
                                                                # (width, y) is the ending point of the line (rightmost 
cv2.imwrite("img/rectangle_image.png", rectangle)
pos_x = widthCAP//2
pos_y = heightCAP//2
imgSplit.append(DragImg("img/rectangle_image.png", [pos_x - width//2, pos_y - height//2]))

# Split the image into smaller parts, create draggable objects for each part, and store them in imgSplit
for ih in range(H_SIZE):
    for iw in range(W_SIZE):
        x = width / W_SIZE * iw
        y = height / H_SIZE * ih
        h = height / H_SIZE
        w = width / W_SIZE

        # Ensure unique and unused position
        rand_w, rand_h = random.randint(0, widthCAP - (int(w)+1)), random.randint(0, heightCAP - (int(h)+1))
        
        while not good_pos(used_positions, rand_w, rand_h):
            rand_w, rand_h = random.randint(0, widthCAP - int(w)), random.randint(0, heightCAP - int(h))

        used_positions.append((rand_w, rand_h))

        img = img[int(y):int(y+h), int(x):int(x+w)]
        NAME = str(time.time())
        cv2.imwrite("img/" + str(ih) + str(iw) + ".png", img)
        pathImg = "img/" + str(ih) + str(iw) + ".png"
        imgSplit.append(DragImg(pathImg, [rand_w, rand_h]))
        img = img2

# Main loop for video processing
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    # Check if hands are detected
    if hands:
        lmList = hands[0]['lmList']
        length, info, img = detector.findDistance(lmList[8][:2], lmList[12][:2], img)

        # Check if the distance between thumb and index finger is less than a threshold
        if length < 50:
            cursor = lmList[8]
            # Update the position of the images except the first one
            for imgObject in imgSplit[1:]:
                imgObject.update(cursor)
                
    try:
        # Display the images on the screen
        for i, imgObject in enumerate(imgSplit):
            h, w = map(int, imgObject.size)
            ox, oy = imgObject.posOrigin

            # Blend the first image with transparency, keep others opaque
            if i == 0:
                img[oy:oy+h, ox:ox+w] = cv2.addWeighted(img[oy:oy+h, ox:ox+w], 1, imgObject.img, 1.5, 100)
            else:
                img[oy:oy+h, ox:ox+w] = imgObject.img
                
    except:
        pass

    # Display the resulting image
    cv2.imshow("Image", img)
    
    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()
    

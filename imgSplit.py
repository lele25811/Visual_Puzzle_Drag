import cv2
from cvzone.HandTrackingModule import HandDetector
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

    toggledImg = None

    # Function to initialize the draggable image
    def __init__(self, path, posOrigin):
        self.path = path
        self.posOrigin = posOrigin
        self.img = cv2.imread(self.path)
        self.size = self.img.shape[:2]
        self.fix = False

    def touched(self, cursor):
        ox, oy = self.posOrigin
        h, w = self.size
        # Check if in the region of the image
        if ox < cursor[0] < ox+w and oy < cursor[1] < oy+h:
            if not(DragImg.toggledImg) or (DragImg.toggledImg == self):
                DragImg.toggledImg = self
                return True
        return False
    
    # Function to update the position of the image
    def update(self, cursor):
        h, w = self.size
        # Check if in the region of the image
        if self.touched(cursor) and not self.fix:
            self.posOrigin = cursor[0] - w//2, cursor[1] - h//2
            return True
        return False
    
    def untoggle(self):
        if DragImg.toggledImg == self:
            DragImg.toggledImg = None

    def fixed(self):
        self.fix = True
        
# Function to check if a random position is good and has enough distance from used positions
def good_pos(used_pos, rand_w, rand_h, min_distance=150):
    for pos in used_pos:
        distance = math.sqrt((pos[0] - rand_w)**2 + (pos[1] - rand_h)**2)
        if distance < min_distance:
            return False
    return True

# Function to add an image to the list of images
def addImage(image, list, x, y, w, h, pos_x, pos_y, ih, iw):
    img_splitted = image[int(y):int(y+h), int(x):int(x+w)]
    cv2.imwrite("img/" + str(ih) + str(iw) + ".png", img_splitted)
    pathImg = "img/" + str(ih) + str(iw) + ".png"
    list.append(DragImg(pathImg, [pos_x, pos_y]))

# Function to calculate the height and width of each image block based on the grid
def calculate_data(width, height, W_SIZE, H_SIZE):
    # Calculate the height of each image block based on the grid
    h = height / H_SIZE
    # Calculate the width of each image block based on the grid
    w = width / W_SIZE
    return h, w

# Function to check if each image from imgSplit is positioned correctly on recSplit
def check_position(imgSplit, recSplit,img,counter=0):
    for imgObject, recObject in zip(imgSplit, recSplit):
        x_img, y_img = imgObject.posOrigin
        x_rec, y_rec = recObject.posOrigin
        h, w = map(int, imgObject.size)
        # Check if the image is positioned correctly on the rectangle
        if x_rec + w//2 - 10 < x_img + w//2 < x_rec + w//2 + 10 and y_rec + h//2 - 10 < y_img + h//2 < y_rec + h//2 + 10:
            cv2.rectangle(img, (x_rec, y_rec), (x_rec + w, y_rec + h), (0, 255, 0), 2)  # Green rectangle for correct position
            counter += 1    # Increment the counter if the image is positioned correctly '''
            imgObject.fixed()
        else:
            cv2.rectangle(img, (x_rec, y_rec), (x_rec + w, y_rec + h), (0, 0, 255), 2)  # Red rectangle for incorrect position
    return counter

def main(difficulty):
    # Load an image and create a draggable object for it
    imgS = cv2.imread('img/lenna.png')
    # Get the height, width, and number of channels of the image
    height, width, channels = imgS.shape
    # Specify the number of vertical and horizontal splits for the image
    W_SIZE, H_SIZE = difficulty+1,difficulty+1
    # List to store the images
    imgSplit = []
    # List to store the rectangles
    recSplit = []
    # List to store used coordinates
    used_positions = []  
    # Create a black rectangle
    rectangle = np.zeros((height, width, 3), dtype=np.uint8)
    cv2.imwrite("img/rectangle_image.png", rectangle)
    img_rec = cv2.imread('img/rectangle_image.png')
    # Split the rectangle into smaller parts, create draggable objects for each part, and store them in recSplit
    for ih in range(H_SIZE): 
        for iw in range(W_SIZE):
            # Calculate the x-coordinate of the top-left corner of the image block
            x = width / W_SIZE * iw 
            # Calculate the y-coordinate of the top-left corner of the image block
            y = height / H_SIZE * ih
            # Calculate the height and width of each image block based on the grid
            h, w = calculate_data(width, height, W_SIZE, H_SIZE)
            # Calculate the position of the image block
            pos_x = int(widthCAP//2 - width//2 + (w * iw))
            pos_y = int(heightCAP//2 - height//2 + (h * ih) )
            # Add the image to the list of images
            addImage(img_rec, recSplit, x, y, w, h, pos_x, pos_y, ih, iw+3)
            # Ensure unique and unused position
            rand_w, rand_h = random.randint(0, widthCAP - (int(w)+1)), random.randint(0, heightCAP - (int(h)+1))
            # when the position is not good, keep generating new positions
            while not good_pos(used_positions, rand_w, rand_h):
                rand_w, rand_h = random.randint(0, widthCAP - (int(w)+1)), random.randint(0, heightCAP - (int(h)+1))
            # Add the position to the list of used positions
            used_positions.append((rand_w, rand_h))
            # Add the image to the list of images
            addImage(imgS, imgSplit, x, y, w, h, rand_w, rand_h, ih, iw)
    # Main loop for video processing
    while True:
        # Read the frame
        success, img = cap.read()
        # Flip the frame
        img = cv2.flip(img, 1)
        # Find the hands in the frame
        hands, img = detector.findHands(img, flipType=False)
        # Check if hands are detected
        if hands:
            # The list of landmarks for the first hand
            lmList = hands[0]['lmList']
            # Get the distance between the index and middle fingers
            length, info, img = detector.findDistance(lmList[8][:2], lmList[12][:2], img)
            # Check if the distance between the index and middle fingers is less than 50
            if length < 50:
                # The cursor is the tip of the index finger
                cursor = lmList[8]
                # Update the position of the images
                for imgObject in imgSplit:
                    DragImg.untoggle(imgObject)
                    if imgObject.update(cursor):
                        break
        try:
            # Draw randomly positioned images on the screen
            for imgObject in imgSplit:
                h, w = map(int, imgObject.size)
                ox2, oy2 = imgObject.posOrigin
                img[oy2:oy2+h, ox2:ox2+w] = imgObject.img
        except:
            pass
        
        # Check if the images are positioned correctly on the rectangles, based on the number of images
        if check_position(imgSplit, recSplit,img) == H_SIZE * W_SIZE:
            # show the original image of the puzzle
            cv2.imshow("Original Image", imgS)
            
        # Display the game window
        cv2.imshow("Image", img)
        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # Release the video capture and close all windows
    cap.release()
    cv2.destroyAllWindows()
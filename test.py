import cv2
from cvzone.HandTrackingModule import HandDetector
import copy
from imgSplit import main as startGame

class ButtonManager:
    def __init__(self):
        self.btnList = []

    def addBtn(self,b):
        if isinstance(b, Button):
            self.btnList.append(b)
        else:
            print("Error: Object is not an instance of Button class.")

    def drawButtons(self):
        for btn in self.btnList:
            btn.draw()

    def ovverideButtons(self,nuoviBtn):
        for btn in nuoviBtn:
            if not isinstance(btn, Button):
                print("Error: Object is not an instance of Button class.")
        self.btnList = copy.deepcopy(nuoviBtn)
       

    def checkClick(self,cursor):
        for btn in self.btnList:
            if btn.posOrigin[0] - btn.size[0]//2 < cursor[0] < btn.posOrigin[0] + btn.size[0]//2 and btn.posOrigin[1] - btn.size[1]//2 < cursor[1] < btn.posOrigin[1] + btn.size[1]//2:
                btn.action()
                break
            
              
    def clearButtons(self):
        self.btnList = []

           
#Superclasse bottone
class Button:
    def __init__(self,title,posOrigin,manager):
        self.title = title
        self.posOrigin = posOrigin
        self.size = (200, 100)
        if isinstance(manager,ButtonManager):
            manager.addBtn(self)

    #draws an ellipse with the title of the button
    def draw(self,baloonColor=(255, 0, 0)):
        cx, cy = self.posOrigin
        w, h = self.size
        ellipse_center = self.posOrigin
        ellipse_axes = (w//2, h//2)
 
        # Find the maximum possible font size to fit the title within the ellipse
        font_size = 4
        while True:
            text_size = cv2.getTextSize(self.title, cv2.FONT_HERSHEY_PLAIN, font_size, 4)[0]
            if text_size[0] < w and text_size[1] < h:
                break
            font_size -= 1

        cv2.ellipse(img, ellipse_center, ellipse_axes, 0, 0, 360, baloonColor, cv2.FILLED)
        cv2.putText(img, self.title, (cx - text_size[0]//2, cy + text_size[1]//2), cv2.FONT_HERSHEY_PLAIN, font_size, (255, 255, 255), 4)

    def action(self):
        pass


#SottoclasseBottoneSettings
class SettingsButton(Button):
    def __init__(self,title,posOrigin,manager):
        super().__init__(title,posOrigin,manager)

    def action(self):
        precButtons = copy.deepcopy(btnManager.btnList)
        btnManager.clearButtons()
        #crea un oggetto DifficultyButton
        difficultyButton = DifficultyButton("Difficulty", (600, 250), btnManager)
        #crea un oggetto HintButton
        hintButton = HintButton("Hint: Off", (600, 400), btnManager)
        #crea un oggetto ExitButton
        exitButton = ExitButton("Exit", (600, 550), btnManager,precButtons)

        

class PlayButton(Button):
    def __init__(self,title,posOrigin,manager):
        super().__init__(title,posOrigin,manager)
        
    def action(self):
        global difficulty
        startGame(cap,difficulty,hints)
       
        
class DifficultyButton(Button):
    def __init__(self,title,posOrigin,manager):
        super().__init__(title,posOrigin,manager)
        
    def action(self):
        precButtons = copy.deepcopy(btnManager.btnList)
        btnManager.clearButtons()
        #crea un oggetto EasyButton
        easyButton = DifficultyModeButton("Easy", (350, 250), btnManager,1)
        #crea un oggetto MediumButton
        mediumButton = DifficultyModeButton("Medium", (600, 250), btnManager,2)
        #crea un oggetto HardButton
        hardButton = DifficultyModeButton("Hard", (850, 250), btnManager,3)
        #crea un oggetto ExitButton
        exitButton = ExitButton("Exit", (600, 400), btnManager,precButtons)
        

class ExitButton(Button):
    def __init__(self,title,posOrigin,manager,precButtons):
        super().__init__(title,posOrigin,manager)
        self.precButtons = precButtons
        

    def action(self):
        btnManager.ovverideButtons(self.precButtons)

class DifficultyModeButton(Button):
    def __init__(self,title,posOrigin,manager,diff):
        super().__init__(title,posOrigin,manager)
        self.diff = diff
        
    def action(self):
        global difficulty
        difficulty = self.diff

    def draw(self):
        if difficulty == self.diff:
            return super().draw((0, 255, 0))
        else:
            return super().draw()
        
class HintButton(Button):
    def __init__(self,title,posOrigin,manager):
        super().__init__(title,posOrigin,manager)
        self.toggle = False
        
    def action(self):
        self.toggle = not self.toggle
        global hints
        if self.toggle:
            
            hints = True
            self.title = "Hint: On"
        else:
            
            hints = False
            self.title = "Hint: Off"
        
        
# Set up the video capture
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Initialize the hand detector from the cvzone library
detector = HandDetector(detectionCon=0.50)

#crea un oggetto ButtonManager
btnManager = ButtonManager()
#crea un oggetto PlayButton
playButton = PlayButton("Play", (600, 250), btnManager)
#crea un oggetto SettingsButton
settingsButton = SettingsButton("Settings", (600, 400), btnManager)

hints = False

clicked = False

difficulty = 1

while True:
    success, img = cap.read()
    if not success:
        cap = cv2.VideoCapture(0)
        cap.set(3, 1280)
        cap.set(4, 720)
        continue
    #Flip the frame
    img = cv2.flip(img, 1)
    # Find the hands in the frame
    hands, img = detector.findHands(img, flipType=False)
    btnManager.drawButtons()
    if hands:
        # The list of landmarks for the first hand
        lmList = hands[0]['lmList']
        # Get the distance between the index and middle fingers
        length, info, img = detector.findDistance(lmList[8][:2], lmList[12][:2], img)
        # Check if the distance between the index and middle fingers is less than 50
        if length < 30:
            #se nella precedente iterazione non è stato cliccato
            if not clicked:
                clicked = True
                # The cursor is the tip of the index finger
                cursor = lmList[8]
                #Check if a button is clicked and execute the action
                btnManager.checkClick(cursor)
                print("clicked")
        else:
            clicked = False
                
    
    cv2.imshow("Image", img)
    
    if cv2.waitKey(1) & 0xFF == ord('s'):
        print("s")
        break
    
    
# Release the video capture and close all windows
print("end")
cap.release()
cv2.destroyAllWindows() 



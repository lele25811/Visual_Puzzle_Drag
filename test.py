import cv2
from cvzone.HandTrackingModule import HandDetector
import copy
from imgSplit import main as startGame
import os

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
        #crea un oggetto ImgButton
        #imgButton = ImgButton("Image", (400, 250), btnManager)
        imgButton = ImgButton("Image", (400, 250), btnManager)
        #crea un oggetto DifficultyButton
        difficultyButton = DifficultyButton("Difficulty", (800, 250), btnManager)
        #crea un oggetto HintButton
        hintButton = HintButton("Hint: Off", (400, 400), btnManager)
        #crea un oggetto ExitButton
        exitButton = ExitButton("Exit", (800, 400), btnManager,precButtons)

        

class PlayButton(Button):
    def __init__(self,title,posOrigin,manager):
        super().__init__(title,posOrigin,manager)
        
    def action(self):
        global difficulty
        global imgChoose
        startGame(cap,difficulty,hints, imgChoose)


class ImgButton(Button):
    def __init__(self,title,posOrigin,manager):
        super().__init__(title,posOrigin,manager)
        
    def action(self):
        precButtons = copy.deepcopy(btnManager.btnList)
        btnManager.clearButtons()
        #crea slider
        slider = Slider("Slider", (600, 250), btnManager)
        #crea tasto incremento slidr
        sliderIncrement = SliderIncrement(">", (1000, 250), btnManager,slider)
        #crea tasto decremento slider
        sliderDecrement = SliderDecrement("<", (200, 250), btnManager,slider)
        #crea tasto conferma(exit mascherato)
        confirmButton = ExitButton("Confirm", (600, 600), btnManager,precButtons)

class Slider(Button):
    def __init__(self, title, posOrigin, manager):
        super().__init__(title, posOrigin, manager)
        self.counter = 0
        self.immagini = []
        for filename in os.listdir("img"):
            print(filename)
            if filename.endswith((".png",".jpg",".jpeg")):
                path = os.path.join("img",filename)
                pic = cv2.imread(path)
                self.immagini.append(pic)

    

    def draw(self):
        self.changeImg()
        imm  = self.immagini[self.counter]
        immResized = cv2.resize(imm, (300,300))
        img[150:150+immResized.shape[0], 450:450+immResized.shape[1]] = immResized  # Sovrappone l'immagine di Lenna sul pulsante

    def changeImg(self):
        global imgChoose
        imgChoose = self.immagini[self.counter]

    
        
class SliderIncrement(Button):
    def __init__(self,title,posOrigin,manager,slider):
        super().__init__(title,posOrigin,manager)
        self.slider = slider
        
    def action(self):
        if self.slider.counter + 1 >= len(self.slider.immagini):
            self.slider.counter = 0
        else:
            self.slider.counter += 1
        #self.slider.changeImg()

    def draw(self):
        super().draw()

class SliderDecrement(Button):
    def __init__(self,title,posOrigin,manager,slider):
        super().__init__(title,posOrigin,manager)
        self.slider = slider
        
    def action(self):
        if self.slider.counter - 1 < 0:
            self.slider.counter = len(self.slider.immagini) - 1
        else:
            self.slider.counter -= 1
        #self.slider.changeImg()

    def draw(self):
        super().draw()
    


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
        self.toggle = True if hints else False
        self.title = "Hint: On" if hints else "Hint: Off"
        
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

imgChoose = None

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
import pygame
import pygame.freetype
from pygame.locals import *
import sys 
import math
import os
from pygame.examples.testsprite import flags
from pickle import TRUE

title = "Hacker-War"
Spieler_Name = os.getlogin()
class SceneBase:
    def __init__(self):
        self.next = self
    
    def ProcessInput(self, events, pressed_keys):
        print("uh-oh, you didn't override this in the child class")

    def Update(self):
        print("uh-oh, you didn't override this in the child class")

    def Render(self, screen):
        print("uh-oh, you didn't override this in the child class")

    def SwitchToScene(self, next_scene):
        active_objects.clear()
        self.next = next_scene
    
    def Terminate(self):
        self.SwitchToScene(None)

def run_game(width, height, fps, starting_scene):
    pygame.init()
    global screen
    screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h))
    clock = pygame.time.Clock()
    active_scene = starting_scene
    active_scene.Render(screen)
    while active_scene != None:
        pressed_keys = pygame.key.get_pressed()
    
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            if event.type == pygame.QUIT:
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressed_keys[pygame.K_LALT] or \
                              pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_F4 and alt_pressed:
                    quit_attempt = True
            
            if quit_attempt:
                active_scene.Terminate()
            else:
                filtered_events.append(event)
        
        active_scene.ProcessInput(filtered_events, pressed_keys)
        active_scene.Update()
        
        active_scene.Render(screen)
        active_scene = active_scene.next
        pygame.display.flip()
        clock.tick(fps)

def wait(__ticks):
        __t = pygame.time.get_ticks() + __ticks
        while pygame.time.get_ticks() < __t:
            pass
        

active_objects=[]
_image_library=[]
def getObj():
    clickcheck = None
    for i in active_objects:
                    if i.button[0]<pygame.mouse.get_pos()[0]<(i.button[0]+i.button[2]) and i.button[1]<pygame.mouse.get_pos()[1]<(i.button[1]+i.button[3]):
                        clickcheck = i
    return clickcheck
def correctInstance(i):
    if isinstance(i, Rect) or isinstance(i, Img):
        return True
    else:
        return False
    
class Text:
    def __init__(self,text,x,y,size,font,color):
        self.text = text
        self.pos = (x*0.01*screen.get_height()+((screen.get_width()-screen.get_height())/2),y*0.01*screen.get_height())
        self.fontcolor = color
        self.font = pygame.font.SysFont(font, size)
        self.img = self.font.render(text, True, self.fontcolor)
        self.rect = self.img.get_rect()
        self.rect.topleft = self.pos
        screen.blit(self.img, self.rect)

_InputBoxes=[]
class InputBox:
    def __init__(self, x, y, width, height, size, font, coloraktiv, colorinaktiv, ActionId: int, text='',):
        self.aid = ActionId
        self.rect = pygame.Rect(x*0.01*screen.get_height()+((screen.get_width()-screen.get_height())/2), y*0.01*screen.get_height(), width*0.01*screen.get_height(), height*0.01*screen.get_height())
        self.button = (x*0.01*screen.get_height()+((screen.get_width()-screen.get_height())/2), y*0.01*screen.get_height(), width*0.01*screen.get_height(), height*0.01*screen.get_height())
        self.coloraktiv = coloraktiv
        self.colorinaktiv =colorinaktiv
        self.font = pygame.font.SysFont(font, size)
        
        try:
            self.active = _InputBoxes[int(self.aid)].active
            self.active
        except AttributeError: self.active = None
        except IndexError: self.active = ":("
        try:
            self.text = _InputBoxes[int(self.aid)].text
            self.text
        except AttributeError: self.text = text
        except IndexError: self.text = text
        
        if self.active == True:
            self.color = coloraktiv
        elif self.active == False:
            self.color = colorinaktiv
        else:
            self.color = colorinaktiv
            
        try: self.txt_surface = self.font.render(self.text, True, self.color)
        except AttributeError: self.txt_surface = self.font.render(text, True, self.color)
        try:
            self = _InputBoxes[int(self.aid)]
        except IndexError:
            self.active = False
            self.text = text
            self.aid = ActionId
            active_objects.append(self)
            _InputBoxes.insert(int(self.aid) ,self)
        self.update()
        self.draw(screen)
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = self.coloraktiv
            else:
                self.active = False
                self.color = self.colorinaktiv
            
            
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    pass
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.color)
                if self.rect.width < self.txt_surface.get_width()+10:
                    self.text = self.text[:-1]
                self.txt_surface = self.font.render(self.text, True, self.color)
        try:
            _InputBoxes[int(self.aid)] = self
        except IndexError: print("Einfüge-Fehler"+str(self))
    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)        

class Img:
    def __init__(self,x,y,width,height,path, ActionId = None):
        self.path = path
        self.button = (x*0.01*screen.get_height()+((screen.get_width()-screen.get_height())/2), y*0.01*screen.get_height(), width*0.01*screen.get_height(), height*0.01*screen.get_height())
        self.aid = ActionId
        self.picture = pygame.transform.scale(self.get_image(self.path),(width*0.01*screen.get_height(), height*0.01*screen.get_height()))
        self.rect = self.picture.get_rect()
        screen.blit(self.picture, (x*0.01*screen.get_height()+((screen.get_width()-screen.get_height())/2),y*0.01*screen.get_height()))
        active_objects.append(self)
    def get_image(self,path):
        test = False
        for i in range(len(_image_library)-1):
            if _image_library[i][0] == path:
                test = TRUE
                return _image_library[i][1]
        if test == False:
                canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
                image = pygame.image.load(canonicalized_path)
                _image_library.append((path,image))
                return image
        
class Rect:
    def __init__(self,x,y,width,height,color, ActionId = None):
        self.button = (x*0.01*screen.get_height()+((screen.get_width()-screen.get_height())/2), y*0.01*screen.get_height(), width*0.01*screen.get_height(), height*0.01*screen.get_height())
        self.aid = ActionId
        pygame.draw.rect(screen, color, pygame.Rect(x*0.01*screen.get_height()+((screen.get_width()-screen.get_height())/2), y*0.01*screen.get_height(), width*0.01*screen.get_height(), height*0.01*screen.get_height()))
        active_objects.append(self)

#class Folder:
        #def __init__(self, path):
            #self.path = path
            
        #def print_folder_content(self):
            
            #files = os.listdir(self.path)
            #for file in files:
                #self.text = Text(file,10,0,40,"Adobe Garamond Pro",(74,74,74))
class Ordner:
    def __init__(self, ordnerpfad):
        self.ordnerpfad = ordnerpfad
        self.inhalt = os.listdir(ordnerpfad)
        self.unterordner = []
        
        # Füge den ersten Unterordner hinzu, wenn vorhanden
        for objekt in self.inhalt:
            objektpfad = os.path.join(self.ordnerpfad, objekt)
            if os.path.isdir(objektpfad):
                self.unterordner.append(objekt)
                break
    
    def ordnerinhalt(self):
        #print("Inhalt des Ordners:")
        for i in self.inhalt[:5]:
            kkl=0
            if kkl==0:
            #print(i)
                self.text = Text(self.inhalt[0],15,21.5,40,"Adobe Garamond Pro",(74,74,74))
                kkl=kkl+1
            if kkl==1 and len(self.inhalt)>1:
                self.text = Text(self.inhalt[1],15,29.5,40,"Adobe Garamond Pro",(74,74,74))
                kkl=kkl+1
            if kkl==2 and len(self.inhalt)>2:
                self.text = Text(self.inhalt[2],15,37.5,40,"Adobe Garamond Pro",(74,74,74))
                kkl=kkl+1
            if kkl==3 and len(self.inhalt)>3:
                self.text = Text(self.inhalt[3],15,45.5,40,"Adobe Garamond Pro",(74,74,74))
                kkl=kkl+1
            if kkl==4 and len(self.inhalt)>4:
                self.text = Text(self.inhalt[4],15,53.5,40,"Adobe Garamond Pro",(74,74,74))
                kkl=kkl+1
            if kkl==5 and len(self.inhalt)>5:
                self.text = Text(self.inhalt[5],15,61.5,40,"Adobe Garamond Pro",(74,74,74))
                kkl=kkl+1
        #if len(self.unterordner) > 0:
            # Zeige den ersten Unterordner an
            #unterordnerpfad = os.path.join(self.ordnerpfad, self.unterordner[0])
            #unterordner = Ordner(unterordnerpfad)
            #unterordner.ordnerinhalt()

#--------------------------------------------------------------------
#--------------------------------------------------------------------
#--------------------------------------------------------------------
Neustart = False
import time
from cmath import nan
class LinuxHauptbildschirm(SceneBase):
    def __init__(self):
        self.time = pygame.time.get_ticks()
        self.Seitenleiste = None
        self.clock = pygame.time.Clock()
        self.window = False
        self.windowdata = 0
        try: self.network
        except AttributeError: self.network = None
        SceneBase.__init__(self)
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                #self.Terminate()
                pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clickcheck=getObj()
                    if correctInstance(self.clickcheck):
                        if  self.clickcheck.aid != None:
                            if self.clickcheck.aid == 1:
                                if self.Seitenleiste == 1:
                                    self.Seitenleiste = None
                                else:
                                    self.Seitenleiste = 1
                            elif self.clickcheck.aid == 2:
                                if self.Seitenleiste == 2:
                                    self.Seitenleiste = None
                                else:
                                    self.Seitenleiste = 2
                            elif self.clickcheck.aid == 3:
                                if self.Seitenleiste == 3:
                                    self.Seitenleiste = None
                                else:
                                    self.Seitenleiste = 3
                            elif self.clickcheck.aid == 4:
                                if self.Seitenleiste != None:
                                    self.Seitenleiste = None
                            elif self.clickcheck.aid == 5:
                                self.window = False
                            else: 
                                if self.clickcheck.aid == 11:
                                    Neustart = False
                                    self.SwitchToScene(LinuxQuitscreen())
                                if self.clickcheck.aid == 12:
                                    Neustart = True
                                    self.SwitchToScene(LinuxQuitscreen())
                                    
                                if self.clickcheck.aid == 13:
                                    self.SwitchToScene(Festplattenauswahl())
                                if self.clickcheck.aid == 14:
                                    self.window = True
                                    self.windowdata = 1
                                
                                if self.clickcheck.aid == 21:
                                    self.SwitchToScene(Dateien())
                                if self.clickcheck.aid == 22:
                                    self.SwitchToScene(Email())
                                if self.clickcheck.aid == 23:
                                    self.SwitchToScene(Dino_Game())
                                if self.clickcheck.aid == 24:
                                    self.window = True
                                    self.windowdata = "Kommandozeile"
                                
                                if self.clickcheck.aid == 31:
                                    self.SwitchToScene(Aircrack_ng())
                                if self.clickcheck.aid == 32:
                                    self.SwitchToScene(Nessus())
                                if self.clickcheck.aid == 33:
                                    self.window = True
                                    self.windowdata = "Cain & Abel"
                                if self.clickcheck.aid == 34:
                                    self.window = True
                                    self.windowdata = "THC Hydra"
                                if self.clickcheck.aid == 35:
                                    self.SwitchToScene(SQL1())
                                if self.clickcheck.aid == 36:
                                    self.window = True
                                    self.windowdata = "TSpy"
                                if self.clickcheck.aid == 37:
                                    self.window = True
                                    self.windowdata = "HULK"
                                if self.clickcheck.aid == 38:
                                    self.window = True
                                    self.windowdata = "Avast"
    def Update(self):
        pass
    def Render(self, screen):
        screen.fill((0, 0, 0))
        self.rect = Rect(0,0,100,100,(0,0,0),4)
        self.img = Img(0,0,100,100,"ubuntu-wallpaper.png",4)

        self.rect = Rect(0,0,100,2,(255,125,0))
        self.rect = Rect(0,0,15,2,(255, 125, 0),1)
        self.text = Text("Einstellungen",0.5,0,18,"couriernew",(255,255,255))
        
        self.rect = Rect(15,0,15,2,(255, 125, 0),2)
        self.text = Text("Programme",15.5,0,18,"couriernew",(255,255,255))

        self.rect = Rect(30,0,15,2,(255, 125, 0),3)
        self.text = Text("Werkzeuge",30.5,0,18,"couriernew",(255,255,255))
        
        self.rect = Rect(45,0,0.2,2,(0, 0, 0))
        self.rect = Rect(15,0,0.2,2,(0, 0, 0))
        self.rect = Rect(30,0,0.2,2,(0, 0, 0))
        
        #self.clock.tick(1)
        self.theTime=time.strftime("%H:%M", time.localtime())
        self.text = Text(str(self.theTime),94,0,18,"couriernew",(255,255,255))
        if self.network == None:
            self.text = Text(str("Nicht verbunden"),75,0,18,"couriernew",(255,255,255))
        else: 
            self.text = Text("↑↓"+str(self.network),75,0,18,"couriernew",(255,255,255))
        if self.Seitenleiste != None:
            self.width = 40
            if self.Seitenleiste == 1:
                self.width = 4*(2.1)
            elif self.Seitenleiste == 2:
                self.width = 4*(2.1)
            elif self.Seitenleiste == 3:
                self.width = 8*(2.1)
            self.rectx = Rect(0,2,20.5,self.width+0.5,(255,125,0))
            self.rect = Rect(0,2,20,self.width,(80, 80, 80))
            #self.text = Text("{}".format(self.Seitenleiste),0,3,18,"couriernew",(255,255,255))
            if self.Seitenleiste == 1:
                self.rect = Rect(0,2,20,2,(125, 125, 125),11)
                self.text = Text("Ausschalten",0,2,18,"couriernew",(255,255,255))
                self.rect = Rect(0,4.1,20,2,(125, 125, 125),12)
                self.text = Text("Neustart",0,4.1,18,"couriernew",(255,255,255))
                self.rect = Rect(0,6.2,20,2,(125, 125, 125),13)
                self.text = Text("Festplattenauswahl",0,6.2,18,"couriernew",(255,255,255))
                self.rect = Rect(0,8.3,20,2,(125, 125, 125),14)
                self.text = Text("Information",0,8.3,18,"couriernew",(255,255,255))
            elif self.Seitenleiste == 2:
                self.rect = Rect(0,2,20,2,(125, 125, 125),21)
                self.text = Text("Dateien",0,2,18,"couriernew",(255,255,255))
                self.rect = Rect(0,4.1,20,2,(125, 125, 125),22)
                self.text = Text("E-Mail",0,4.1,18,"couriernew",(255,255,255))
                self.rect = Rect(0,6.2,20,2,(125, 125, 125),23)
                self.text = Text("Browser",0,6.2,18,"couriernew",(255,255,255))
                self.rect = Rect(0,8.3,20,2,(125, 125, 125),24)
                self.text = Text("Kommandozeile",0,8.3,18,"couriernew",(255,255,255))
            elif self.Seitenleiste == 3:
                self.rect = Rect(0,2,20,2,(125, 125, 125),31)
                self.text = Text("Aircrack-ng",0,2,18,"couriernew",(255,255,255))
                self.rect = Rect(0,4.1,20,2,(125, 125, 125),32)
                self.text = Text("Nessus",0,4.1,18,"couriernew",(255,255,255))
                self.rect = Rect(0,6.2,20,2,(125, 125, 125),33)
                self.text = Text("Cain & Abel",0,6.2,18,"couriernew",(255,255,255))
                self.rect = Rect(0,8.3,20,2,(125, 125, 125),34)
                self.text = Text("THC Hydra",0,8.3,18,"couriernew",(255,255,255))
                self.rect = Rect(0,10.4,20,2,(125, 125, 125),35)
                self.text = Text("SQLMap",0,10.4,18,"couriernew",(255,255,255))
                self.rect = Rect(0,12.5,20,2,(125, 125, 125),36)
                self.text = Text("TSpy",0,12.5,18,"couriernew",(255,255,255))
                self.rect = Rect(0,14.6,20,2,(125, 125, 125),37)
                self.text = Text("HULK",0,14.6,18,"couriernew",(255,255,255))
                self.rect = Rect(0,16.7,20,2,(125, 125, 125),38)
                self.text = Text("Avast",0,16.7,18,"couriernew",(255,255,255))
        if self.window == True:
            self.rect = Rect(29.8,32.8,40.5,32.5,(255, 125, 0))
            self.rect = Rect(30,35,40,30,(125, 125, 125))
            self.rect = Rect(66,32.8,4.3,2.3,(255, 0, 0),5)
            self.text = Text("X",67.5,32.6,25,"couriernew",(255,255,255))
            if self.windowdata == 1:
                #Titel
                self.text = Text("Information",30,32.8,18,"couriernew",(255,255,255))
                #Inhalt:
                self.text = Text("Operating System: Ubuntu Linux",30,35,18,"couriernew",(255,255,255))
                self.text = Text("Manufactory: Alaito Corporation",30,37,18,"couriernew",(255,255,255))
                self.text = Text("Version: 0.1.x",30,39,18,"couriernew",(255,255,255))
                self.text = Text("Follow Ali on Instagram: @ALI.16.04",30,41,18,"couriernew",(255,255,255))
            elif self.windowdata.isnumeric() == False:
                
                #Titel
                self.text = Text(str(self.windowdata),30,32.8,18,"couriernew",(255,255,255))
                #Inhalt:
                self.text = Text("Error: Programm nicht gefunden",30,35,18,"couriernew",(255,255,255))
        
#---------------

class LinuxLadescreen(SceneBase):
    def __init__(self):
        self.time = pygame.time.get_ticks()
        self.progress = 0
        self.Loadtime = 10 #Je größer desto schneller
        SceneBase.__init__(self)
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Move to the next scene when the user pressed Enter
                #self.SwitchToScene(TitleScene())
                #self.Terminate()
                pass
    def Update(self):
        pass
    def Render(self, screen):
        # The game scene is just a blank blue screen
        screen.fill((0, 0, 0))
        #run_game.clock
        if self.time+1000<pygame.time.get_ticks():
            self.text = Text("ubuntu",35,40,50,"couriernew",(255,125,0))
            self.img = Img(55,40,7,7,"ubuntu-logo32.png")
            self.text = Text("Wird gestartet...",35,50,30,"couriernew",(255,255,255))
            self.rect = Rect(35,55,27,3,(187,187,187))
            self.rect = Rect(35.5,55.5,26,2,(0, 0, 0))
            self.rect = Rect(35.5,55.5,(26/100)*self.progress,2,(255, 125, 0))
        if self.progress <= 100:
            self.progress = math.floor(((pygame.time.get_ticks()-(self.time+1000))/1000)*self.Loadtime)
        else:
            wait(1000)
            self.SwitchToScene(LinuxHauptbildschirm())

#---------------

class Loadup(SceneBase):
    def __init__(self):
        self.time = pygame.time.get_ticks()
        self.ready = False
        SceneBase.__init__(self)
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and self.ready == True:
                # Move to the next scene when the user pressed Enter
                self.SwitchToScene(Festplattenauswahl())
    def Update(self):
        pass
    def Render(self, screen):
        # The game scene is just a blank blue screen
        
        screen.fill((0, 0, 0))
        #run_game.clock
        if self.time+100<pygame.time.get_ticks():
            self.text1 = Text("Alaito Corporation",0,5,30,"Arial",(255,255,255))
            self.text1 = Text("All Rights Reserved",0,10,30,"Arial",(255,255,255))
            self.text1 = Text("Getting Boot data...",0,15,30,"Arial",(255,255,255))
        if self.time+1100<pygame.time.get_ticks():
            self.text1 = Text("",0,20,30,"Arial",(255,255,255))
        if self.time+3100<pygame.time.get_ticks():
            self.text1 = Text(title,0,25,30,"Arial",(255,255,255))
            self.text1 = Text("a Game by Aiden, Ali and Tobias",0,30,30,"Arial",(255,255,255))
            self.text1 = Text("Made in IF1 EA Class",0,35,30,"Arial",(255,255,255))
        if self.time+4100<pygame.time.get_ticks():
            self.text1 = Text("",0,40,30,"Arial",(255,255,255))
            self.text1 = Text("Used Programs and Databases:",0,45,30,"Arial",(255,255,255))
            self.text1 = Text("Eclipse and Pygame",0,50,30,"Arial",(255,255,255))
        if self.time+6100<pygame.time.get_ticks():
            self.text1 = Text("",0,55,30,"Arial",(255,255,255))
            self.text1 = Text("Version: 0.5.3",0,60,30,"Arial",(255,255,255))
            self.text1 = Text("Setup-Version: 1.4",0,65,30,"Arial",(255,255,255))
            self.text1 = Text("Pygame-Version: 1.6.9",0,70,30,"Arial",(255,255,255))
            self.text1 = Text("Eclipse-Version: 2022-12",0,75,30,"Arial",(255,255,255))
            self.text1 = Text("Follow Ali on Instagram: @ALI.16.04",0,80,30,"Arial",(255,255,255))
        if self.time+7100<pygame.time.get_ticks():
            self.text1 = Text("",0,85,30,"Arial",(255,255,255))
            self.text1 = Text("Press any Button to Continue...",0,90,30,"Arial",(255,255,255))
            self.ready = True

#---------------

class Festplattenauswahl(SceneBase):
    def __init__(self):
        self.time = pygame.time.get_ticks()
        self.ready = False
        SceneBase.__init__(self)
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and self.ready == True:
                # Move to the next scene when the user pressed Enter
                self.SwitchToScene(LinuxLadescreen())
                
    def Update(self):
        pass
    def Render(self, screen):
        # The game scene is just a blank blue screen
        
        screen.fill((0, 0, 0))
        #run_game.clock
        if self.time+100<pygame.time.get_ticks():
            self.text1 = Text("Alaito Corporation",0,5,30,"Arial",(255,255,255))
            self.text1 = Text("Suchen Sie eine Festplatte aus, welche sie benutzen möchten",0,10,30,"Arial",(255,255,255))
            self.text1 = Text("Festplatten laden...",0,15,30,"Arial",(255,255,255))
        if self.time+1100<pygame.time.get_ticks():
            self.text1 = Text("",0,20,30,"Arial",(255,255,255))
        if self.time+3100<pygame.time.get_ticks():
            self.rect = Rect(10,45,20,10,(255,255,255),1)
            self.text1 = Text("Festplatte 1",10,55,30,"Arial",(255,255,255))
            self.rect = Rect(40,45,20,10,(255,255,255),1)
            self.text1 = Text("Festplatte 2",40,55,30,"Arial",(255,255,255))
            self.rect = Rect(70,45,20,10,(255,255,255),1)
            self.text1 = Text("Festplatte 3",70,55,30,"Arial",(255,255,255))
        if self.time+7100<pygame.time.get_ticks():
            self.text1 = Text("",0,85,30,"Arial",(255,255,255))
            self.text1 = Text("Drücken sie die Zahl welche Festplatte Sie verwenden möchten",0,90,30,"Arial",(255,255,255))
            self.ready = True

#-----------------------------------

class LinuxQuitscreen(SceneBase):
    def __init__(self):
        self.time = pygame.time.get_ticks()
        self.progress = 0
        self.Loadtime = 10 #Je größer desto schneller
        SceneBase.__init__(self)
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Move to the next scene when the user pressed Enter
                #self.SwitchToScene(TitleScene())
                #self.Terminate()
                pass
    def Update(self):
        pass
    def Render(self, screen):
        # The game scene is just a blank blue screen
        screen.fill((0, 0, 0))
        #run_game.clock
        if self.time+1000<pygame.time.get_ticks():
            self.text = Text("ubuntu",35,40,50,"couriernew",(255,125,0))
            self.img = Img(55,40,7,7,"ubuntu-logo32.png")
            self.animation = self.progress%16
            if self.animation >= 0 and self.animation <= 3:
                self.text = Text("Wird heruntergefahren",35,50,30,"couriernew",(255,255,255))
            elif self.animation >= 4 and self.animation <= 7:
                 self.text = Text("Wird heruntergefahren.",35,50,30,"couriernew",(255,255,255))
            elif self.animation >= 8  and self.animation <= 11:
                 self.text = Text("Wird heruntergefahren..",35,50,30,"couriernew",(255,255,255))
            elif self.animation >= 12 and self.animation <= 15:
                 self.text = Text("Wird heruntergefahren...",35,50,30,"couriernew",(255,255,255))
            else:
                pass
        if self.progress <= 100:
            self.progress = math.floor(((pygame.time.get_ticks()-(self.time+1000))/1000)*self.Loadtime)
        else:
            wait(1000)
            if Neustart == True:
                self.SwitchToScene(Loadup())
            else:
                self.Terminate()

#------------------------
import random
class Aircrack_ng(SceneBase):
    def __init__(self):
        self.time = None
        self.ip = None
        self.ip2 = None
        self.timecounter = None
        self.coretime = None
        self.core1 = False
        self.core2 = False
        self.core3 = False
        self.core4 = False
        self.core5 = False
        self.core6 = False
        self.core7 = False
        self.core8 = False
        self.attack = None
        SceneBase.__init__(self)
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            try: self.IB.handle_event(event)
            except AttributeError: pass
            if event.type == pygame.KEYDOWN:
                pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.clickcheck=getObj()
                if correctInstance(self.clickcheck):
                    if  self.clickcheck.aid != None:
                        if self.clickcheck.aid == "close":
                            try: self.SwitchToScene(LinuxHauptbildschirm())
                            except NameError: self.Terminate()
                        if self.clickcheck.aid == 2:
                            self.ip = self.IB.text
                            self.IB.text=""
                        if self.clickcheck.aid == 11:
                            self.core1 = True
                        if self.clickcheck.aid == 12:
                            self.core2 = True
                        if self.clickcheck.aid == 13:
                            self.core3 = True
                        if self.clickcheck.aid == 14:
                            self.core4= True
                        if self.clickcheck.aid == 15:
                            self.core5 = True
                        if self.clickcheck.aid == 16:
                            self.core6 = True
                        if self.clickcheck.aid == 17:
                            self.core7 = True
                        if self.clickcheck.aid == 18:
                            self.core8 = True
                            
    def Update(self):
        pass
    def Render(self, screen):
        screen.fill((0, 0, 0))
        self.rect = Rect(0,0,100,100,(5,5,5))
        #---------------------------------------------------------
        self.text = Text("Bitte Netzwerk IP eingeben:",25,2,30,"couriernew",(0,255,0))
        self.IB = InputBox(25,5,40,5,20,"couriernew",(0,240,0),(0,255,0),1)
        self.rect = Rect(65,5,7,5,(0,255,0),2)
        self.text = Text("=>",66,5.2,40,"couriernew",(255,255,255))
        if self.ip != None:
            self.legit = True
            self.ips = []
            self.ips = self.ip.split(".")
            if len(self.ips) == 4:
                for i in self.ips:
                    try:
                        if (int(i) >=0 and int(i) <=255) == False:
                            self.legit = False
                    except ValueError: self.legit = False
            else: self.legit = False
            if self.legit == True:
                if self.ip != self.ip2:
                    self.time = pygame.time.get_ticks()
                    self.coretime = 0
                    self.timecounter = 0
                    self.done = False
                    self.attack = random.randint(1,5)
                if pygame.time.get_ticks()-self.time <= 1000:
                    self.text = Text("Wird Verbunden...",25,10,30,"couriernew",(0,255,0))
                else:
                    if self.ip == "133.74.218.7":
                        if self.done == False:
                            self.text = Text("Verarbeite IP: "+self.ip,25,10,30,"couriernew",(0,255,0))
                            if pygame.time.get_ticks()-self.time>= 3000:
                                self.text = Text("Schwachstelle endeckt:",25,15,30,"couriernew",(0,255,0))
                                if self.attack == 1:
                                    self.text = Text("DNS aktiv",25,20,30,"couriernew",(0,255,0))
                                if self.attack == 2:
                                    self.text = Text("Router nicht geupdated",25,20,30,"couriernew",(0,255,0))
                                if self.attack == 3:
                                    self.text = Text("Firewall falsch konfiguriert",25,20,30,"couriernew",(0,255,0))
                                if self.attack == 4:
                                    self.text = Text("Ungeschützter Port",25,20,30,"couriernew",(0,255,0))
                                if self.attack == 5:
                                    self.text = Text("'Port 23: Telnet' aktiv",25,20,30,"couriernew",(0,255,0))
                            if pygame.time.get_ticks()-self.time>= 4000:
                                self.text = Text("Starte Angriff...",25,25,30,"couriernew",(0,255,0))
                            if pygame.time.get_ticks()-self.time>= 5000:
                                self.rect = Rect(25,30,50,50,(125,125,125))
                                self.rect = Rect(25,30,50,5,(32,32,32))
                                self.akerne = 0
                                if pygame.time.get_ticks() % 10 == 0:
                                    if random.randint(0,10)==0:
                                        self.r = random.randint(1,8)
                                        if self.r ==1:
                                            self.core1 = False
                                        if self.r ==2:
                                            self.core2 = False
                                        if self.r ==3:
                                            self.core3 = False
                                        if self.r ==4:
                                            self.core4 = False
                                        if self.r ==5:
                                            self.core5 = False
                                        if self.r ==6:
                                            self.core6 = False
                                        if self.r ==7: 
                                            self.core7 = False
                                        if self.r ==8:
                                            self.core8 = False
                                if self.core1 == True: 
                                    self.akerne = self.akerne + 1
                                    self.rect = Rect(26,36,23.5,10,(0,255,0))
                                else:
                                    self.rect = Rect(26,36,23.5,10,(255,0,0),11)
                                if self.core2 == True: 
                                    self.akerne = self.akerne + 1
                                    self.rect = Rect(26,47,23.5,10,(0,255,0))
                                else:
                                    self.rect = Rect(26,47,23.5,10,(255,0,0),12)
                                if self.core3 == True: 
                                    self.akerne = self.akerne + 1
                                    self.rect = Rect(26,58,23.5,10,(0,255,0))
                                else:
                                    self.rect = Rect(26,58,23.5,10,(255,0,0),13)
                                if self.core4 == True: 
                                    self.akerne = self.akerne + 1
                                    self.rect = Rect(26,69,23.5,10,(0,255,0))
                                else:
                                    self.rect = Rect(26,69,23.5,10,(255,0,0),14)
                                if self.core5 == True: 
                                    self.akerne = self.akerne + 1
                                    self.rect = Rect(50.5,36,23.5,10,(0,255,0))
                                else:
                                    self.rect = Rect(50.5,36,23.5,10,(255,0,0),15)
                                if self.core6 == True: 
                                    self.akerne = self.akerne + 1
                                    self.rect = Rect(50.5,47,23.5,10,(0,255,0))
                                else:
                                    self.rect = Rect(50.5,47,23.5,10,(255,0,0),16)
                                if self.core7 == True: 
                                    self.akerne = self.akerne + 1
                                    self.rect = Rect(50.5,58,23.5,10,(0,255,0))
                                else:
                                    self.rect = Rect(50.5,58,23.5,10,(255,0,0),17)
                                if self.core8 == True: 
                                    self.akerne = self.akerne + 1
                                    self.rect = Rect(50.5,69,23.5,10,(0,255,0))
                                else:
                                    self.rect = Rect(50.5,69,23.5,10,(255,0,0),18)
                                self.text = Text("Kerne Aktiv: "+str(self.akerne)+"/8",25,30.5,30,"couriernew",(0,255,0))
                                if self.akerne == 8:
                                    self.coretime = pygame.time.get_ticks()-self.timecounter
                                else: self.timecounter = pygame.time.get_ticks()-self.coretime
                                if 20-math.floor(self.coretime/1000) >=10:
                                    self.text = Text("00:"+str(20-math.floor(self.coretime/1000)),65,30.5,30,"couriernew",(0,255,0))
                                else: 
                                    self.text = Text("00:0"+str(20-math.floor(self.coretime/1000)),65,30.5,30,"couriernew",(0,255,0))
                                if 20-math.floor(self.coretime/1000) <= 0:
                                    self.done = True
                        else:
                            self.text = Text("Verbunden mit: "+self.ip,25,10,30,"couriernew",(0,255,0))
                            LinuxHauptbildschirm.network = self.ip
                    else:
                        self.text = Text("Netzwerk nicht gefunden",25,10,30,"couriernew",(0,255,0))
            else: self.text = Text("Eingegebene Daten sind keine IP",25,10,30,"couriernew",(0,255,0))
        self.ip2 = self.ip
        #---------------------------------------------------------
        self.rect = Rect(0,0,100,2,(255,125,0))
        self.rect = Rect(95.8,0,4.3,2,(255, 0, 0),"close")
        self.text = Text("X",97.2,-0.3,25,"couriernew",(255,255,255))
        self.text = Text("Aircrack-ng",0.5,0,18,"couriernew",(255,255,255))

#------------------------
class Nessus(SceneBase):
    def __init__(self):
        self.time = None
        self.timestamp = None
        self.search = False
        self.network = LinuxHauptbildschirm.network
        self.device = None
        self.ip = None
        self.ipl = None
        self.x = 20
        self.tx = None
        self.vx = 15
        self.y1 = 20
        self.y2 = 20
        self.y3 = 20
        self.y4 = 20
        self.vy = 50
        self.ts1 = None
        self.ts2 = None
        self.ts3 = None
        self.ts4 = None
        SceneBase.__init__(self)
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.clickcheck=getObj()
                if correctInstance(self.clickcheck):
                    if  self.clickcheck.aid != None:
                        if self.clickcheck.aid == "close":
                            try: self.SwitchToScene(LinuxHauptbildschirm)
                            except NameError: self.Terminate()
                        elif self.clickcheck.aid == 0:
                            self.search = True
                        elif self.clickcheck.aid >=1 and self.clickcheck.aid<=10:
                            self.device = self.clickcheck.aid
                        elif self.clickcheck.aid == 11:
                            if self.ts1 == None:
                                self.ts1 = pygame.time.get_ticks()
                        elif self.clickcheck.aid == 12:
                            if self.ts2 == None:
                                self.ts2 = pygame.time.get_ticks()
                        elif self.clickcheck.aid == 13:
                            if self.ts3 == None:
                                self.ts3 = pygame.time.get_ticks()
                        elif self.clickcheck.aid == 14:
                            if self.ts4 == None:
                                self.ts4 = pygame.time.get_ticks()
    def Update(self):
        pass
    def Render(self, screen):
        screen.fill((0, 0, 0))
        #---------------------------------------------------------
        self.rect = Rect(25,5,50,5,(0,255,255),0)
        self.text = Text("Netzwerk durchsuchen",27,5.5,35,"couriernew",(0,0,0))
        if self.search == True:
            if self.time == None:
                self.timestamp = pygame.time.get_ticks()
                self.time = pygame.time.get_ticks()-self.timestamp
            else: 
                self.time = pygame.time.get_ticks()-self.timestamp
            if self.network == None:
                self.text = Text("Nicht mit Netzwerk verbunden!",27,10,35,"couriernew",(0,255,255))
            else:
                if self.time < 3000:
                    if math.floor(self.time/100) % 4 == 0:
                        self.text = Text("Suche nach Geräten",27,10,35,"couriernew",(0,255,255))
                    if math.floor(self.time/100) % 4 == 1:
                        self.text = Text("Suche nach Geräten.",27,10,35,"couriernew",(0,255,255))
                    if math.floor(self.time/100) % 4 == 2:
                        self.text = Text("Suche nach Geräten..",27,10,35,"couriernew",(0,255,255))
                    if math.floor(self.time/100) % 4 == 3:
                        self.text = Text("Suche nach Geräten...",27,10,35,"couriernew",(0,255,255))
                if self.time >= 3000:
                    if self.ip == None:
                        self.ipl = self.network.split(".")
                        self.ip = self.ipl[0]+"."+self.ipl[1]+"."+self.ipl[2]+"."
                    if self.device == None:
                        self.rect = Rect(25,15,50,5,(0,0,0),1)
                        self.rect = Rect(25,20,50,5,(0,0,0),2)
                        self.rect = Rect(25,25,50,5,(0,0,0),3)
                        self.rect = Rect(25,30,50,5,(0,0,0),4)
                        self.text = Text(self.ip+"12",27,15,35,"couriernew",(0,255,255))
                        self.text = Text(self.ip+"63",27,20,35,"couriernew",(0,255,255))
                        self.text = Text(self.ip+"117",27,25,35,"couriernew",(0,255,255))
                        self.text = Text(self.ip+"235",27,30,35,"couriernew",(0,255,255))
                    else:
                        if self.ts1 != None:
                            self.t = pygame.time.get_ticks()-self.ts1
                            self.d = (self.t/1000) * self.vy
                            if self.d >= 40:
                                self.y1 = 20
                                self.ts1 = None
                            elif self.d >= 20:
                                self.y1 = 60-self.d
                            else: self.y1 = 20+self.d
                        if self.ts2 != None:
                            self.t = pygame.time.get_ticks()-self.ts2
                            self.d = (self.t/1000) * self.vy
                            if self.d >= 40:
                                self.y2 = 20
                                self.ts2 = None
                            elif self.d >= 20:
                                self.y2 = 60-self.d
                            else: self.y2 = 20+self.d
                        if self.ts3 != None:
                            self.t = pygame.time.get_ticks()-self.ts3
                            self.d = (self.t/1000) * self.vy
                            if self.d >= 40:
                                self.y3 = 20
                                self.ts3 = None
                            elif self.d >= 20:
                                self.y3 = 60-self.d
                            else: self.y3 = 20+self.d
                        if self.ts4 != None:
                            self.t = pygame.time.get_ticks()-self.ts4
                            self.d = (self.t/1000) * self.vy
                            if self.d >= 40:
                                self.y4 = 20
                                self.ts4 = None
                            elif self.d >= 20:
                                self.y4 = 60-self.d
                            else: self.y4 = 20+self.d
                        if self.tx != None:
                            self.t = pygame.time.get_ticks()-self.tx
                            self.d = (self.t/1000) * self.vx
                            if self.d >= 55:
                                
                                self.SwitchToScene(WindowsHauptbildschirm())
                            else:
                                self.x = 20 + self.d
                                self.xd = False
                                if self.x >= 27 and self.x <= 32 and self.y1 < 25: self.xd = True
                                if self.x >= 39 and self.x <= 44 and self.y2 < 25: self.xd = True
                                if self.x >= 51 and self.x <= 56 and self.y3 < 25: self.xd = True
                                if self.x >= 63 and self.x <= 68 and self.y4 < 25: self.xd = True
                                if self.xd == True:
                                    self.tx = None
                                    self.x = 20
                        else: 
                            self.tx = pygame.time.get_ticks()
                            self.x = 20
                        self.rect = Rect(25,15,50,50,(125,125,125))
                        self.rect = Rect(25,20,50,5,(0,0,0))
                        
                        
                        self.rect = Rect(27,60,10,5,(255,0,0),11)
                        self.rect = Rect(39,60,10,5,(255,255,0),12)
                        self.rect = Rect(51,60,10,5,(0,255,0),13)
                        self.rect = Rect(63,60,10,5,(0,0,255),14)
                        
                        self.rect = Rect(30,20,5,25,(0,0,0))
                        self.rect = Rect(42,20,5,25,(0,0,0))
                        self.rect = Rect(54,20,5,25,(0,0,0))
                        self.rect = Rect(66,20,5,25,(0,0,0))
                        
                        self.rect = Rect(self.x,20,5,5,(255,255,255))
                        
                        self.rect = Rect(30,self.y1,5,5,(255,0,0))
                        self.rect = Rect(42,self.y2,5,5,(255,255,0))
                        self.rect = Rect(54,self.y3,5,5,(0,255,0))
                        self.rect = Rect(66,self.y4,5,5,(0,0,255))
                        
        #---------------------------------------------------------
        self.rect = Rect(0,0,100,2,(255,125,0))
        self.rect = Rect(95.8,0,4.3,2,(255, 0, 0),"close")
        self.text = Text("X",97.2,-0.3,25,"couriernew",(255,255,255))
        self.text = Text("Nessus",0.5,0,18,"couriernew",(255,255,255))
#------------------------
class WindowsHauptbildschirm(SceneBase):
    def __init__(self):
        self.time = pygame.time.get_ticks()
        self.Seitenleiste = None
        self.clock = pygame.time.Clock()
        self.window = False
        self.windowdata = 0
        self.network = LinuxHauptbildschirm.network
        SceneBase.__init__(self)
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                pass
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clickcheck=getObj()
                    if correctInstance(self.clickcheck):
                        if  self.clickcheck.aid != None:
                            if self.clickcheck.aid == 1:
                                if self.Seitenleiste == 1:
                                    self.Seitenleiste = None
                                else:
                                    self.Seitenleiste = 1
                            elif self.clickcheck.aid == 2:
                                if self.Seitenleiste == 2:
                                    self.Seitenleiste = None
                                else:
                                    self.Seitenleiste = 2
                            elif self.clickcheck.aid == 3:
                                if self.Seitenleiste == 3:
                                    self.Seitenleiste = None
                                else:
                                    self.Seitenleiste = 3
                            elif self.clickcheck.aid == 4:
                                if self.Seitenleiste != None:
                                    self.Seitenleiste = None
                            elif self.clickcheck.aid == 5:
                                self.window = False
                            else: 
                                if self.clickcheck.aid == 11:
                                    self.SwitchToScene(LinuxHauptbildschirm())
                                if self.clickcheck.aid == 12:
                                    #screen.fill(0,0,0)
                                    #wait(2000)
                                    self.SwitchToScene(LinuxHauptbildschirm())
                                    pass
                                if self.clickcheck.aid == 13:
                                    pass
                                if self.clickcheck.aid == 14:
                                    self.window = True
                                    self.windowdata = 1
                                
                                if self.clickcheck.aid == 21:
                                    self.window = True
                                    self.windowdata = "Dateien"
                                if self.clickcheck.aid == 22:
                                    self.window = True
                                    self.windowdata = "E-Mail"
                                if self.clickcheck.aid == 23:
                                    self.window = True
                                    self.windowdata = "Browser"
                                
    def Update(self):
        pass
    def Render(self, screen):
        screen.fill((0, 0, 0))
        self.rect = Rect(0,0,100,100,(64,64,64),4)
        #self.rect = Rect(0,0,100,50,(0,255,255),4)
        #self.rect = Rect(0,50,100,50,(20,255,0),4)
        #self.img = Img(0,0,100,100,"ubuntu-wallpaper.png",4)
        
        self.rect = Rect(0,95,100,5,(34,88,214))
        self.rect = Rect(0,95,5,5,(27,136,27),1)
        self.rect = Rect(0.2,95.2,2.2,2.2,(0,255,0),1)
        self.rect = Rect(2.6,95.2,2.2,2.2,(255,0,0),1)
        self.rect = Rect(0.2,97.6,2.2,2.2,(255,255,0),1)
        self.rect = Rect(2.6,97.6,2.2,2.2,(0,0,255),1)
        
        #self.clock.tick(1)
        self.rect = Rect(79,95,21,5,(12,153,235))
        self.theTime=time.strftime("%H:%M", time.localtime())
        self.text = Text(str(self.theTime),92.5,95,22,"couriernew",(255,255,255))
        self.theTime=time.strftime("%d.%m.%Y", time.localtime())
        self.text = Text(str(self.theTime),86,97.3,22,"couriernew",(255,255,255))
        self.text = Text("↑↓",80,96,24,"couriernew",(255,255,255))
        if self.Seitenleiste != None:
            self.width = 12
            self.rectx = Rect(0,95-(self.width+2),22,self.width+2,(34,88,214))
            self.rect = Rect(0,95-self.width,21.5,self.width,(125, 125, 125))
            self.text = Text("Menü",0,95-(self.width+2),18,"couriernew",(255,255,255))
            #self.text = Text("{}".format(self.Seitenleiste),0,3,18,"couriernew",(255,255,255))
            if self.Seitenleiste == 1:
                self.rect = Rect(0,95-(2*6),20,2,(125, 125, 125),22)
                self.text = Text("E-Mail",0,95-(2*6),18,"couriernew",(255,255,255))
                self.rect = Rect(0,95-(2*5),20,2,(125, 125, 125),23)
                self.text = Text("Browser",0,95-(2*5),18,"couriernew",(255,255,255))
                self.rect = Rect(0,95-(2*4),20,2,(125, 125, 125),21)
                self.text = Text("Explorer",0,95-(2*4),18,"couriernew",(255,255,255))
 
                self.rect = Rect(0,95-(2*3),20,2,(125, 125, 125),11)
                self.text = Text("Ausschalten",0,95-(2*3),18,"couriernew",(255,255,255))
                self.rect = Rect(0,95-(2*2),20,2,(125, 125, 125),12)
                self.text = Text("Neustart",0,95-(2*2),18,"couriernew",(255,255,255))
                self.rect = Rect(0,95-(2*1),20,2,(125, 125, 125),14)
                self.text = Text("Information",0,95-(2*1),18,"couriernew",(255,255,255))
        if self.window == True:
            self.rect = Rect(29.8,32.8,40.5,32.5,(34,88,214))
            self.rect = Rect(30,35,40,30,(125, 125, 125))
            self.rect = Rect(66,32.8,4.3,2.3,(255, 0, 0),5)
            self.text = Text("X",67.5,32.6,25,"couriernew",(255,255,255))
            if self.windowdata == 1:
                #Titel
                self.text = Text("Information",30,32.8,18,"couriernew",(255,255,255))
                #Inhalt:
                self.text = Text("Operating System: Windows",30,35,18,"couriernew",(255,255,255))
                self.text = Text("Manufactory: Alaito Corporation",30,37,18,"couriernew",(255,255,255))
                self.text = Text("Version: 0.1.x",30,39,18,"couriernew",(255,255,255))
                self.text = Text("Follow Ali on Instagram: @ALI.16.04",30,41,18,"couriernew",(255,255,255))
            elif self.windowdata.isnumeric() == False:
                
                #Titel
                self.text = Text(str(self.windowdata),30,32.8,18,"couriernew",(255,255,255))
                #Inhalt:
                self.text = Text("Error: Programm nicht gefunden",30,35,18,"couriernew",(255,255,255))










#------------------------
class Email(SceneBase):
    def __init__(self):
        self.time = pygame.time.get_ticks()
        self.ready = False
        SceneBase.__init__(self)
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.clickcheck=getObj()
                if correctInstance(self.clickcheck):
                    if  self.clickcheck.aid == 1:
                        self.SwitchToScene(Email_oeffnen())
                
    def Update(self):
        pass
    def Render(self, screen):
        # The game scene is just a blank blue screen
        screen.fill((0,0,0))
        self.rect = Rect(0,0,100,100,(255,255,255))
        self.img = Img(0,0,100,100,"Email-logo.jpg")
        #run_game.clock
        if self.time+2100<pygame.time.get_ticks():
            screen.fill((0,0,0))
            self.rect = Rect(0,0,100,100,(255,255,255))
            self.text1 = Text("Alaito Corporation",0,5,30,"Arial",(0,0,0))
            self.text1 = Text("Email Postfach von "+Spieler_Name,0,10,30,"Arial",(0,0,0))
            self.text1 = Text("Emails werden empfangen...",0,15,30,"Arial",(0,0,0))
        if self.time+3100<pygame.time.get_ticks():
            self.text1 = Text("1 neue Nachricht",0,20,30,"Arial",(0,0,0))
        if self.time+4100<pygame.time.get_ticks():
            self.rect = Rect(0,30,60,5,(100,100,100),1)
            self.text1 = Text("Unbekannt: ein kleiner Tipp",0,30,30,"Arial",(0,0,0))
            self.ready = True

class Email_oeffnen(SceneBase):
    def __init__(self):
        self.time = pygame.time.get_ticks()
        self.ready = False
        SceneBase.__init__(self)
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.clickcheck=getObj()
                if correctInstance(self.clickcheck):
                    if  self.clickcheck.aid == 1:
                        self.SwitchToScene(LinuxHauptbildschirm())
                
    def Update(self):
        pass
    def Render(self, screen):
        # The game scene is just a blank blue screen
        screen.fill((0,0,0))
        self.rect = Rect(0,0,100,100,(255,255,255))
        #self.rect = Rect(0,0,100,100,(0,0,0),4)
        self.img = Img(0,0,90,40,"Email-oeffnen.png")
        #run_game.clock
        if self.time+100<pygame.time.get_ticks():
            self.rect = Rect(0,30,100,10,(255,255,255))
            self.text1 = Text("Von: unbekannt@alaito.corporation.de",10,16,20,"Arial",(0,0,0))
            self.text1 = Text("Betreff: ein kleiner Tipp",0,30,30,"Arial",(0,0,0))
            #self.text1 = Text("Kein Anhang",0,30,30,"Arial",(0,0,0))
        if self.time+1100<pygame.time.get_ticks():
            self.text1 = Text("Ich bin überzeugt von deiner Unschuld und würde dir gerne einen kleinen Tipp geben",0,40,30,"Arial",(0,0,0))
            self.text1 = Text("um den richigen Taeter zu finden. Du kannst dir Zugang zu unserem Netwerk beschaffen.",0,45,30,"Arial",(0,0,0))
            self.text1 = Text("Die Ip ist 133.74.218.7.Ich hoffe du findest genug",0,50,30,"Arial",(0,0,0))
            self.text1 = Text("Beweise um deine Unschuld zu beweisen.",0,55,30,"Arial",(0,0,0))
            self.text1 = Text("Dein Unbekannter Helfer",0,62,30,"Arial",(0,0,0))
        if self.time+4100<pygame.time.get_ticks():
            self.rect = Rect(0,80,65,5,(100,100,100),1)
            self.text1 = Text("Drücken um die Nachricht zu schließen",0,80,30,"Arial",(0,0,0))
            self.ready = True
#------------------------
class SQL1(SceneBase):
    def __init__(self):
        self.time = pygame.time.get_ticks()
        self.ready = False
        self.game = False
        
        SceneBase.__init__(self)
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and self.ready == True:
                # Move to the next scene when the user pressed Enter
                #self.SwitchToScene(Email_oeffnen())
                self.game = True
    def Update(self):
        pass
    def Render(self, screen):
        # The game scene is just a blank blue screen
        screen.fill((0, 0, 0))
        #self.rect = Rect(0,0,100,100,(0,0,0),4)
        #self.img = Img(5,7,10,10,"Datenbank.png")
        
        #run_game.clock
        if self.time+100<pygame.time.get_ticks():
            self.text1 = Text("um Zugriff auf SQL zu erlangen musst du die pinken Vierecke zusammen führen",0,5,30,"Arial",(255,255,255))
            self.text1 = Text("Steuern tust du durch die Pfeiltasten.",0,10,30,"Arial",(255,255,255))
        if self.time+3100<pygame.time.get_ticks():
            self.text1 = Text("Drücken Sie Enter um Fortzufahren",0,50,30,"Arial",(255,255,255))
            self.ready = True
        if self.game == True:
            self.main(screen)

    def main(self, screen):    
        self.game = False  
        bg = [0,0,0]     
        gamePlayer = Sprite([40*0.01*screen.get_height()+((screen.get_width()-screen.get_height())/2), 50*0.01*screen.get_height()],screen)  
        gamePlayer.move = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]  
        gamePlayer.vx = 5 
        gamePlayer.vy = 5 
        wx = random.randint(5,90)*0.01*screen.get_height()+((screen.get_width()-screen.get_height())/2)
        wy = random.randint(5,90)*0.01*screen.get_height()
        wall = Sprite([wx,wy],screen)  
       
        wall_group = pygame.sprite.Group()  
        wall_group.add(wall)  
       
        gamePlayer_group = pygame.sprite.Group()  
        gamePlayer_group.add(gamePlayer)  
        self.run = True
        while self.run == True:  
            for event in pygame.event.get():  
                if event.type == pygame.QUIT:  
                    return False  
            key = pygame.key.get_pressed()  
            for i in range(2):  
                if key[gamePlayer.move[i]]:  
                    gamePlayer.rect.x += gamePlayer.vx * [-1, 1][i]  
       
            for i in range(2):  
                if key[gamePlayer.move[2:4][i]]:  
                    gamePlayer.rect.y += gamePlayer.vy * [-1, 1][i]  
            if gamePlayer.rect.x > 95*0.01*screen.get_height()+((screen.get_width()-screen.get_height())/2):
                gamePlayer.rect.x = 95*0.01*screen.get_height()+((screen.get_width()-screen.get_height())/2)
            if gamePlayer.rect.x < 0*0.01*screen.get_height()+((screen.get_width()-screen.get_height())/2):
                gamePlayer.rect.x = 0*0.01*screen.get_height()+((screen.get_width()-screen.get_height())/2)
            if gamePlayer.rect.y > 95*0.01*screen.get_height():
                gamePlayer.rect.y = 95*0.01*screen.get_height()
            if gamePlayer.rect.y < 0*0.01*screen.get_height():
                gamePlayer.rect.y = 0*0.01*screen.get_height()
            screen.fill(bg)  
            self.rect = Rect(0,0,100,100,(255,255,255))
            collision = pygame.sprite.spritecollide(gamePlayer, wall_group, True)  
            if collision:    
                gamePlayer.image.fill((0, 0, 0))  
                self.run = False
            gamePlayer_group.draw(screen)  
            wall_group.draw(screen)  
            pygame.display.update()  
        self.SwitchToScene(SQL2()) 
        
class SQL2(SceneBase):
    def __init__(self):
        self.time = pygame.time.get_ticks()
        self.ready = False
        SceneBase.__init__(self)
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Move to the next scene when the user pressed Enter
                self.SwitchToScene(LinuxHauptbildschirm())
    def Update(self):
        pass
    def Render(self, screen):
        screen.fill((0,0,0))
        self.text1 = Text("SQL-Datenbank",0,5,30,"Arial",(255,255,255))
        self.text1 = Text("Bald Verfügbar!",0,10,30,"Arial",(255,255,255))
        self.text1 = Text("Drücke eine Taste um zurück zum Hauptbildschirm zu kommen",0,15,30,"Arial",(255,255,255))
  
    
class Sprite(pygame.sprite.Sprite):  
    def __init__(self, pos, screen):  
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.Surface([5*0.01*screen.get_height(), 5*0.01*screen.get_height()])  
        self.image.fill((255, 0, 255))  
        self.rect = self.image.get_rect()  
        self.rect.center = pos  

#----------------------

class Dateien(SceneBase):
    def __init__(self):
        self.time = pygame.time.get_ticks()
        self.Seitenleiste = None
        self.clock = pygame.time.Clock()
        self.window = False
        self.windowdata = 0
        #self.ordner = Ordner(r'D:\Eclipse\Info\Dieser PC')
        #self.vhpfad='D:\Eclipse\Info\Dieser PC'
        #self.vspfad='H:\Dieser PC'
        self.opfad = os.path.abspath(__file__)
        self.opfad = self.opfad.split("\\")
        self.opfad.pop()
        self.opfad.append("Dieser PC")
        self.vspfad = os.sep.join(self.opfad)
        self.ordner = Ordner(self.vspfad)
        SceneBase.__init__(self)
    def Update(self):
        pass
    def Render(self, screen):
        
        # The game scene is just a blank blue screen
        screen.fill((0,0,0))
        self.rect = Rect(0,0,100,100,(255,255,255))
        #self.rect = Rect(0,0,100,4,(255,180,255),4)
        
        if len(self.ordner.inhalt)>0:
            self.rect = Rect(10,20,80,6,(255,200,255),10)
            
        if len(self.ordner.inhalt)>1:
            self.rect = Rect(10,28,80,6,(255,200,255),11)
        
        if len(self.ordner.inhalt)>2:
            self.rect = Rect(10,36,80,6,(255,200,255),12)
        
        if len(self.ordner.inhalt)>3:
            self.rect = Rect(10,44,80,6,(255,200,255),13)
        
        if len(self.ordner.inhalt)>4:
            self.rect = Rect(10,52,80,6,(255,200,255),14)
        
        if len(self.ordner.inhalt)>5:
            self.rect = Rect(10,60,80,6,(255,200,255),15)
        
        
        #if self.ordner.ordnerpfad!=(r'D:\Eclipse\Info\Dieser PC'):
        if self.ordner.ordnerpfad!=(self.vspfad):
            self.rect = Rect(10,90,15,5,(200,10,10), 1)
            self.text = Text("Zurück",10,90,40,"couriernew",(255,255,255))
            
            
            
        #self.rect = Rect(10,68,50,6,(255,200,255))
        
        self.rect = Rect(10,7,80,5,(150, 225, 0),1)
        #self.text = Text("Einstellungen",0.5,0,18,"couriernew",(255,255,255))
        
        #self.rect = Rect(85,0,15,4,(255, 0, 0),2)
        #self.text = Text("X",85.4,0.4,40,"Adobe Garamond Pro",(255,255,255))
        #self.text = Text("Dateien",0,0.4,40,"Adobe Garamond Pro",(255,255,255))
        
        self.rect = Rect(0,0,100,2,(255,125,0))
        self.rect = Rect(95.8,0,4.3,2,(255, 0, 0),"close")
        self.text = Text("X",97.2,-0.3,25,"couriernew",(255,255,255))
        self.text = Text("Dateien",0.5,0,18,"couriernew",(255,255,255))
        
        self.ordnerview = self.ordner.ordnerpfad.replace(self.vspfad, "C:\\Dieser PC")
        self.font = pygame.font.SysFont("couriernew", 20)
        self.img = self.font.render(self.ordnerview, True, (0,0,0))
        if self.img.get_width() <= 80*0.01*screen.get_height():
            self.d = Text(self.ordnerview,10,8,20,"couriernew",(74,74,200))
        else: 
            while self.img.get_width() > 80*0.01*screen.get_height():
                self.overwrite = self.ordnerview.split(os.sep)
                self.overwrite.pop(0)
                self.ordnerview = os.sep.join(self.overwrite)
                self.font = pygame.font.SysFont("couriernew", 20)
                self.img = self.font.render(self.ordnerview, True, (0,0,0))    
            self.d = Text(self.ordnerview,10,8,20,"couriernew",(74,74,200))
            
        self.ordner.ordnerinhalt()
        #path = os.getcwd()
        #filename = 'iconv.dll'
        
        #file_path = os.path.join(path, filename)
        #print(file_path)
        
        #for i in glob.glob(r'D:\Eclipse\Info\Dieser PC\*'):

        #open_folder(Setup.root_folder)
        #class open_folder:
    #def open_folder(self, folder_path):
        #global root_folder
        #contents = os.listdir(folder_path)
        #print("Inhalt des Ordners: ")
        #for item in contents:
            #print(item)
    
    
    
        #selected_path = os.path.join(folder_path, selected_item)
        #if os.path.isdir(selected_path):
            
    

        #root_folder = "D:\Eclipse\Info\Dieser PC\System"
        
        
            #if offnen ==1:
                #Ordner = os.path.join(Ordner, Ordner.inhalt[0])
                        
        
        
        


            
            
            
            
            
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.ordner = Ordner(os.path.split(self.ordner.ordnerpfad)[0])
                #if event.key == pygame.K_p:
                    #self.Terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.clickcheck=getObj()
                if correctInstance(self.clickcheck):
                    if  self.clickcheck.aid != None:
                        if self.clickcheck.aid == "close":
                            try: self.SwitchToScene(LinuxHauptbildschirm())
                            except NameError: self.Terminate()
                        if self.clickcheck.aid == 1:
                            self.ordner = Ordner(os.path.split(self.ordner.ordnerpfad)[0])
                        if self.clickcheck.aid == 10:
                            if os.path.isfile(str(os.path.join(self.ordner.ordnerpfad, self.ordner.inhalt[0])))==False:
                                self.ordner = Ordner(str(os.path.join(self.ordner.ordnerpfad, self.ordner.inhalt[0])))
                        if self.clickcheck.aid == 11:
                            if os.path.isfile(str(os.path.join(self.ordner.ordnerpfad, self.ordner.inhalt[1])))==False:
                                self.ordner = Ordner(str(os.path.join(self.ordner.ordnerpfad, self.ordner.inhalt[1])))
                        if self.clickcheck.aid == 12:
                            if os.path.isfile(str(os.path.join(self.ordner.ordnerpfad, self.ordner.inhalt[2])))==False:
                                self.ordner = Ordner(str(os.path.join(self.ordner.ordnerpfad, self.ordner.inhalt[2])))
                        if self.clickcheck.aid == 13:
                            if os.path.isfile(str(os.path.join(self.ordner.ordnerpfad, self.ordner.inhalt[3])))==False:
                                self.ordner = Ordner(str(os.path.join(self.ordner.ordnerpfad, self.ordner.inhalt[3])))
                        if self.clickcheck.aid == 14:
                            if os.path.isfile(str(os.path.join(self.ordner.ordnerpfad, self.ordner.inhalt[4])))==False:
                                self.ordner = Ordner(str(os.path.join(self.ordner.ordnerpfad, self.ordner.inhalt[4])))
                        if self.clickcheck.aid == 15:
                            if os.path.isfile(str(os.path.join(self.ordner.ordnerpfad, self.ordner.inhalt[5])))==False:
                                self.ordner = Ordner(str(os.path.join(self.ordner.ordnerpfad, self.ordner.inhalt[5])))
                        
                            
                            
                            
                            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and True == False:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x >= 375 and mouse_x <= 375 + 615 and mouse_y >= 150 and mouse_y <= 150 + 45:
                    if len(self.ordner.inhalt) >0:
                        if os.path.isfile(str(os.path.join(self.ordner.ordnerpfad, self.ordner.inhalt[0])))==False:
                            self.ordner = Ordner(str(os.path.join(self.ordner.ordnerpfad, self.ordner.inhalt[0])))
                #print(mouse_x, mouse_y)
                if len(self.ordner.inhalt) >1:
                    if mouse_x >= 375 and mouse_x <= 375 + 615 and mouse_y >= 215 and mouse_y <= 215 + 45:
                        if os.path.isfile(str(os.path.join(self.ordner.ordnerpfad, self.ordner.inhalt[1])))==False:
                            self.ordner = Ordner(str(os.path.join(self.ordner.ordnerpfad, self.ordner.inhalt[1])))
                
                if len(self.ordner.inhalt) >2:        
                    if mouse_x >= 375 and mouse_x <= 375 + 615 and mouse_y >= 275 and mouse_y <= 275 + 45:
                        if os.path.isfile(str(os.path.join(self.ordner.ordnerpfad, self.ordner.inhalt[2])))==False:
                            self.ordner = Ordner(str(os.path.join(self.ordner.ordnerpfad, self.ordner.inhalt[2])))
                
                if len(self.ordner.inhalt) >3:        
                    if mouse_x >= 375 and mouse_x <= 375 + 615 and mouse_y >= 335 and mouse_y <= 335 + 45:
                        if os.path.isfile(str(os.path.join(self.ordner.ordnerpfad, self.ordner.inhalt[3])))==False:
                            self.ordner = Ordner(str(os.path.join(self.ordner.ordnerpfad, self.ordner.inhalt[3])))        
                        
                
                if len(self.ordner.inhalt) >4:            
                    if mouse_x >= 375 and mouse_x <= 375 + 615 and mouse_y >= 400 and mouse_y <= 400 + 45:
                        if os.path.isfile(str(os.path.join(self.ordner.ordnerpfad, self.ordner.inhalt[4])))==False:
                            self.ordner = Ordner(str(os.path.join(self.ordner.ordnerpfad, self.ordner.inhalt[4])))
                
                if len(self.ordner.inhalt) >5:
                    if mouse_x >= 375 and mouse_x <= 375 + 615 and mouse_y >= 460 and mouse_y <= 460 + 45:
                        if os.path.isfile(str(os.path.join(self.ordner.ordnerpfad, self.ordner.inhalt[5])))==False:
                            self.ordner = Ordner(str(os.path.join(self.ordner.ordnerpfad, self.ordner.inhalt[5])))
                
                if mouse_x >= 1344 and mouse_x <= 1344 + 20 and mouse_y >= 0 and mouse_y <= 0 + 28:
                    self.Terminate()
                    
                if mouse_x >= 107 and mouse_x <= 107 + 114 and mouse_y >= 115 and mouse_y <= 115 + 37:
                    self.ordner = Ordner(os.path.split(self.ordner.ordnerpfad)[0])
                    
        #if event.type == pygame.MOUSEBUTTONDOWN AND                                                                                                                                                                         
                                                                                                                                                                                
        #self.text = Text(i,10.4,0.4,40,"Adobe Garamond Pro",(255,255,255))
        #self.rect = Rect(15,0,0.2,2,(0, 0, 0))
        #self.rect = Rect(30,0,0.2,2,(0, 0, 0))

#---------------------------------------

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))


class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1


class Dino_Game(SceneBase):
    def __init__(self):
        self.time = pygame.time.get_ticks()
        self.ready = False
        
        SceneBase.__init__(self)
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Move to the next scene when the user pressed Enter
                #self.SwitchToScene(LinuxHauptbildschirm())
                pass
    def Update(self):
        pass
    def Render(self, screen):
        global SCREEN_HEIGHT 
        global SCREEN_WIDTH 
        global SCREEN 
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        SCREEN_HEIGHT = screen.get_height()
        SCREEN_WIDTH = screen.get_width()
        SCREEN = screen
        run = True
        self.menu(screen = screen,death_count=0, run = run)
        
    def main(self, screen, run):
        global game_speed, x_pos_bg, y_pos_bg, points, obstacles
        clock = pygame.time.Clock()
        player = Dinosaur()
        cloud = Cloud()
        game_speed = 20
        x_pos_bg = 0
        y_pos_bg = 380
        points = 0
        
        obstacles = []
        death_count = 0
        
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            screen.fill((255, 255, 255))
            userInput = pygame.key.get_pressed()
            
            player.draw(screen)
            player.update(userInput)
            
            if len(obstacles) == 0:
                if random.randint(0, 2) == 0:
                    obstacles.append(SmallCactus(SMALL_CACTUS))
                elif random.randint(0, 2) == 1:
                    obstacles.append(LargeCactus(LARGE_CACTUS))
                elif random.randint(0, 2) == 2:
                    obstacles.append(Bird(BIRD))
            
            for obstacle in obstacles:
                obstacle.draw(screen)
                obstacle.update()
                if player.dino_rect.colliderect(obstacle.rect):
                    pygame.time.delay(2000)
                    death_count += 1
                    run = False
                    self.menu(death_count, screen, run)
            
            self.background(screen)
            
            cloud.draw(screen)
            cloud.update()
            
            self.score(screen)
            
            clock.tick(30)
            pygame.display.update()
    
    def score(self, screen):
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        
        text = self.font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        screen.blit(text, textRect)
    
    def background(self, screen):
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        screen.blit(BG, (x_pos_bg, y_pos_bg))
        screen.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed
        

    def menu(self, death_count, screen, run):
        global points
        run = True
        while run == True:
            screen.fill((255, 255, 255))
            font = pygame.font.Font('freesansbold.ttf', 30)
    
            if death_count == 0:
                text = font.render("Press any Key to Start", True, (0, 0, 0))
            elif death_count > 0:
                text = font.render("Press any Key to Restart", True, (0, 0, 0))
                score = font.render("Your Score: " + str(points), True, (0, 0, 0))
                scoreRect = score.get_rect()
                scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT  // 2 + 50)
                screen.blit(score, scoreRect)
            textRect = text.get_rect()
            textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT  // 2)
            screen.blit(text, textRect)
            screen.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT  // 2 - 140))
            pygame.display.update()
            if run == False:
                self.Terminate()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    self.Terminate()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP :
                    if run == True:
                        self.main(screen, run)
                if run == False:
                    self.Terminate()
    


run_game(0,0,60,Loadup())


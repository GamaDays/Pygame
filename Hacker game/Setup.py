import pygame
import pygame.freetype
from pygame.locals import *
import sys 
import math
import os
from pygame.examples.testsprite import flags
from pickle import TRUE

title = "Hacker-War"
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
                #if event.key == pygame.K_ESCAPE:
                    #quit_attempt = True
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
        #Action id implementieren
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
                # Re-render the text.
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
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
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

#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#


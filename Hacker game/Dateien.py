from Full_Game import *
import time
import os
import glob
from cmath import nan
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


run_game(0, 0, 60, Dateien())
from Setup import *

class x1(SceneBase):
    def __init__(self):
        
        self.test = 0
        SceneBase.__init__(self)
    def ProcessInput(self, events, pressed_keys):
        pass
    def Render(self, screen):
        screen.fill((0, 0, 0))
        self.SwitchToScene(x2())
        #---------------------------------------------------------
class x2(SceneBase):
    def __init__(self):
        x1.test = 1
        SceneBase.__init__(self)
    def ProcessInput(self, events, pressed_keys):
        pass
    def Render(self, screen):
        screen.fill((0, 0, 0))  
        
        print(x1.test)     

run_game(0, 0, 60, x1())
import random
import pygame as pg
from .config.settings import *
from .core.gameplay import *
from .core.credits import *
from .core.mainmenu import *
from .core.game_over import *
from .core.instructions import *
from .core.start import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pg.display.set_caption(GAME_TITLE)
        self.clock = pg.time.Clock()
        # self.running = True
        self.current_state = 'start'
        self.action = None
        
        # Screen Initialization
        self.init_screens()
    
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
    
    def init_screens(self):
        self.splash = LunchGame(self)
        self.main_menu = MainMenu(self.screen)
        self.credits = None 
        self.game_over = GameOver()
        self.instruction = Instructions()
    
    def handle_action(self, action):
        
        if self.current_state == 'start':
            action = self.splash.run() 
            
        elif self.current_state == 'menu':
            action = self.main_menu.run()
            
        elif self.current_state == 'credits':
            if self.credits is None: # Petite correction de nom ici (self.credits vs credits_screen)
                self.credits = Credits(self)
            action = self.credits.run()
               
        elif self.current_state == 'game':
            self.game = GamePlay()
            action = self.game.run()
            print("Début du jeu...")
            
        elif self.current_state == 'instruction':
            action = self.instruction.run()
        
        elif self.current_state == 'game_over':
            action = self.game_over.run() # Correction nom variable (ecran_game_over -> game_over)
            
        else:
            action = 'quit'
        
        return action
    
    def handle_current_state(self):
        if self.action == 'menu':
            self.current_state = 'menu'
        elif self.action == 'game':
            self.current_state = 'game'   
        elif self.action == 'credits':
            self.current_state = 'credits'   
        elif self.action == 'instructions':
            self.current_state = 'instruction' 
        elif self.action == "game_over":
            self.current_state = 'game_over'
            self.credits = None 
        elif self.action == 'restart': # Gérer le restart depuis game over
                self.current_state = 'game'        
        elif self.action == 'quit':
            self.running = False
        
        return self.current_state
    
    def update(self):
        self.action = self.handle_action(self.action)
        self.current_state = self.handle_current_state()
        
    
    def run(self):
        while True:
            self.check_events()
            self.update()
            
        
        pg.quit()
        sys.exit()
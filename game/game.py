import random
from .config.settings import *
from .core.gameplay import GamePlay
from .core.credits import Credits
from .core.mainmenu import MainMenu
from .core.game_over import GameOver
from .core.instructions import Instructions
from .core.start import SplashScreen 

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        
        # État initial : on commence par le splash screen !
        self.current_state = 'splash' 
        
        # Initialisation des écrans
        self.splash = SplashScreen()
        self.main_menu = MainMenu(self.screen)
        self.credits = None 
        self.game_over = GameOver()
        self.instruction = Instructions()
    
    def run(self):
        while self.running:
            # Récupère l'état actif
            
            if self.current_state == 'splash': # <--- Gestion de l'état splash
                action = self.splash.run()
                
            elif self.current_state == 'menu':
                action = self.main_menu.run()
                
            elif self.current_state == 'credits':
                if self.credits is None: # Petite correction de nom ici (self.credits vs credits_screen)
                    self.credits = Credits(self.screen)
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

            # Gère la transition d'état
            if action == 'menu':
                self.current_state = 'menu'
            elif action == 'game':
                self.current_state = 'game'
            elif action == 'credits':
                self.current_state = 'credits'
            elif action == 'instructions':
                self.current_state = 'instruction'
            elif action == "game_over":
                self.current_state = 'game_over'
                self.credits = None 
            elif action == 'restart': # Gérer le restart depuis game over
                 self.current_state = 'game'
            elif action == 'quit':
                self.running = False
        
        pygame.quit()
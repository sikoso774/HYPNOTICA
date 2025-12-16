import pygame as pg
import sys
from .config.settings import *
from .core.sound import Sound

# Import des écrans
from .core.start import Intro
from .core.mainmenu import MainMenu
from .core.game_over import GameOver
from .core.instructions import Instructions
from .core.credits import Credits
from .core.level import Level # Nouvelle classe (ex-GamePlay)

class Game:
    def __init__(self):
        pg.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pg.display.set_caption("Deep Hypnotica")
        self.clock = pygame.time.Clock()
        
        # 1. Gestionnaire de son centralisé
        self.sound = Sound(self)
        
        # 2. Initialisation des écrans
        # On passe 'self' pour que les écrans accèdent au sound et au screen
        self.intro = Intro(self)
        self.main_menu = MainMenu(self)
        self.game_over = GameOver(self)
        self.instruction = Instructions(self)
        self.credits = Credits(self)
        
        # Le niveau est instancié mais peut être réinitialisé à chaque nouvelle partie
        self.level = Level(self)

        self.current_state = 'start' # Etat initial

    def run(self):
        """Boucle principale qui délègue le contrôle aux écrans"""
        while True:
            action = None
            
            # --- Machine à états ---
            if self.current_state == 'start':
                action = self.intro.run()
                
            elif self.current_state == 'menu':
                action = self.main_menu.run()
                
            elif self.current_state == 'instruction':
                action = self.instruction.run()
                
            elif self.current_state == 'credits':
                action = self.credits.run()
                
            elif self.current_state == 'game':
                # On recrée le niveau pour reset la partie (optionnel)
                # self.level = Level(self) 
                action = self.level.run()
                
            elif self.current_state == 'game_over':
                action = self.game_over.run()
            
            # --- Gestion des transitions ---
            if action == 'quit':
                self.quit_app()
            elif action:
                self.current_state = action # Changement d'état (ex: "menu" -> "game")

    def quit_app(self):
        pygame.quit()
        sys.exit()
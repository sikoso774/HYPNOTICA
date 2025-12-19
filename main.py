import pygame as pg
import sys

# Config du jeu
from game.config import *
from game.core import Intro, MainMenu, Instructions, GameOver, Credits, Level_3D

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Deep Hypnotica")
        self.clock = pg.time.Clock()
        self.sound = Sound(self)
        self.delta_time = 0.016
        self.setup()
        self.current_state = 'start' # Etat initial
    
    def setup(self):
        self.intro = Intro(self)
        self.main_menu = MainMenu(self)
        self.level = Level_3D(self)
        self.game_over = GameOver(self)
        self.instruction = Instructions(self)
        self.credits = Credits(self)

    def run(self):
        """Boucle principale qui délègue le contrôle aux écrans"""
        while True:
            action = None
            # --- Machine à états ---
            if self.current_state == 'start':
                action = self.intro.run()   
            elif self.current_state == 'menu':
                action = self.main_menu.run()
            elif self.current_state == 'instructions':
                action = self.instruction.run()   
            elif self.current_state == 'credits':
                action = self.credits.run()
                
            elif self.current_state == 'game':
                # On recrée le niveau pour reset la partie (optionnel)
                self.level = Level_3D(self) 
                action = self.level.run()
                
            elif self.current_state == 'game_over':
                action = self.game_over.run()
            
            # --- Gestion des transitions ---
            if action == 'quit':
                pg.quit()
                sys.exit()

            elif action:
                self.current_state = action # Changement d'état (ex: "menu" -> "game")
                
                
if __name__ == "__main__":
    game = Game()
    game.run()
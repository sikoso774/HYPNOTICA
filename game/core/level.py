import pygame as pg
from .base_screen import BaseScreen
from ..components.sprites.sprites import Player, Phone, Background
from ..components.elements.satiety import Satiety
from ..components.sprites.groups import AllSprites
from ..config.settings import FPS

class Level(BaseScreen):
    def __init__(self, game):
        super().__init__(game)
        # La musique 'game' est définie dans SoundHandler (voir étape précédente)
        self.music_name = 'game' 
        # On initialise les sprites
        self.reset()

    def reset(self):
        """Réinitialise le niveau pour une nouvelle partie."""
        self.all_sprites = AllSprites()
        self.satiety_bar = Satiety()
        self.background = Background(self.all_sprites, self.screen)
        self.player = Player(self.all_sprites)
        self.phone = Phone(self.all_sprites)

    def run(self):
        """Surcharge pour reset le niveau avant de lancer la boucle."""
        self.reset()
        return super().run()

    def update(self):
        # Calcul du delta time (basé sur le tick du BaseScreen précédent)
        dt = self.clock.get_time() / 1000

        self.all_sprites.update(dt)
        self.satiety_bar.decrease()

        # Collisions
        if self.player.rect.colliderect(self.phone.rect):
            self.satiety_bar.increase()
            self.phone.reset_position()

        # Conditions de fin
        if self.satiety_bar.is_empty():
            return "game_over" # Renvoie l'action au Game Controller
            
        return None

    def draw(self):
        # L'ordre est important : background (dans all_sprites) -> ui
        self.all_sprites.draw() 
        self.satiety_bar.draw(self.screen)
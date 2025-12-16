import pygame as pg
from ...config.settings import *

# 1. On hérite de LayeredUpdates pour gérer l'ordre d'affichage
class AllSprites(pg.sprite.LayeredUpdates):
    def __init__(self):
        super().__init__()
        self.screen = pg.display.get_surface()
    
    def draw(self):
        # On nettoie l'écran (optionnel si le background couvre tout, mais sécurisant)
        self.screen.fill(COLORS['black'])
        
        # 2. La méthode draw native de LayeredUpdates respecte l'ordre des couches (self._layer)
        # On peut appeler super().draw(self.screen) ou faire la boucle nous-même.
        # super().draw est optimisé, mais ta boucle personnalisée marche aussi.
        # Utilisons ta méthode mais adaptée :
        
        for sprite in self:
            self.screen.blit(sprite.image, sprite.rect)

# class AllSprites(pygame.sprite.Group):
#     def __init__(self):
#         super().__init__()
#         self.screen = pygame.display.get_surface()
    
#     def draw(self):
#         self.screen.fill(COLORS['black'])
#         for sprite in self:
#             self.screen.blit(sprite.image, sprite.rect)
            
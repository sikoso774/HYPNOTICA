import pygame as pg
from ...config.settings import *

class Satiety:
    def __init__(self):
        if not pg.font.get_init():
            pg.font.init()
        self.value = SATIETY_DATA['start']
        self.decrease_rate = SATIETY_DATA['decrease_rate']
        self.increase_amount = SATIETY_DATA['increase_amount']
        self.font = pg.font.Font(DEFAULT_FONT_NAME, 20) # Police pour afficher la valeur de satiété

    def decrease(self):
        """Diminue la valeur de satiété."""
        self.value -= self.decrease_rate
        if self.value < 0:
            self.value = 0 # La satiété ne descend pas en dessous de zéro

    def increase(self):
        """Augmente la valeur de satiété, plafonnée à 100."""
        self.value += self.increase_amount
        if self.value > 100:
            self.value = 100

    def is_empty(self):
        """Vérifie si la satiété est tombée à zéro."""
        return self.value <= 0
    
    def draw(self, surface):
        """
        Dessine la barre de satiété et sa valeur.
        """
        # Dimensions et position de la barre de satiété
        bar_x, bar_y = 10, 10
        bar_width = 200
        bar_height = 20

        # Fond de la barre (toujours rouge pour indiquer la "perte" ou le maximum)
        pg.draw.rect(surface, COLORS['red'], (bar_x, bar_y, bar_width, bar_height))

        # Calcul de la largeur de la partie verte de la barre
        current_width = int(bar_width * (self.value / 100))
        pg.draw.rect(surface, COLORS['green'], (bar_x, bar_y, current_width, bar_height))

        # Contour de la barre
        pg.draw.rect(surface, COLORS['white'], (bar_x, bar_y, bar_width, bar_height), 2) # épaisseur 2

        # Afficher la valeur numérique de la satiété
        satiety_text = f"Satiété: {int(self.value)}%"
        text_surface = self.font.render(satiety_text, True, COLORS['white'])
        text_rect = text_surface.get_rect(topleft=(bar_x + bar_width + 10, bar_y))
        surface.blit(text_surface, text_rect)
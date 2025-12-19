import pygame as pg
from game.config import *

class TextScroller:
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        
        # Chargement de la police
        font_path = get_resource_path(join("assets", "fonts", "MINDCONTROL.ttf"))
        try:
            self.font = pg.font.Font(font_path, 24)
        except FileNotFoundError:
            self.font = pg.font.Font(None, 24)

        # Liste du texte à afficher
        self.text_list = [
            "GAME OVER",
            "",
            "Press R to Replay",
            "",
            "Press A for Credits",
            "",
            "Press Q to Quit",
        ]
        
        self.x = self.width # Commence hors de l'écran à droite
        self.speed = 1 # Vitesse de défilement

    def draw_and_scroll(self, surface):
        """
        Dessine et fait défiler le texte.
        """
        max_text_width = 0

        for i, line in enumerate(self.text_list):
            # Rendu du texte (Couleur VERTE -> COLORS['green'])
            text_surf = self.font.render(line, True, COLORS['green'])
            
            # Positionnement
            # On centre verticalement un peu en bas + décalage par ligne
            text_rect = text_surf.get_rect(y=self.height // 9.5 + i * 30)
            text_rect.x = self.x
            
            surface.blit(text_surf, text_rect)

            # Calcul pour le reset de la boucle
            if text_rect.width > max_text_width:
                max_text_width = text_rect.width

        # Mise à jour de la position
        self.x -= self.speed

        # Réinitialise la position si tout le texte est sorti de l'écran
        if self.x < -max_text_width:
            self.x = self.width
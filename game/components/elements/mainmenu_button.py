from ...config.settings import *
from ...config.utils import get_font # Pour obtenir l'objet police
from ...constants.mainmenu_const import BUTTON_ACTIVE_COLOR, BUTTON_INACTIVE_COLOR
from ...config.support import *

import pygame

class Bouton:
    # Chemin des sons, à importer si tu as un sfx_manager.py
    pygame.mixer.init()
    # SOUND_CLICK = audio_importer(SOUND_DIR)[SOUND_CLICK_FILE]
    # SOUND_HOVER = audio_importer(SOUND_DIR)[SOUND_HOVER_FILE]
    
    # Si je ne veux voir aucun problème avec PyInstaller...
    SOUND_CLICK = pygame.mixer.Sound(get_resource_path(join(SOUND_DIR, SOUND_CLICK_FILE +'.wav')))
    SOUND_HOVER = pygame.mixer.Sound(get_resource_path(join(SOUND_DIR, SOUND_HOVER_FILE +'.wav')))

    # Police doit être chargée ici ou passée en paramètre. 
    # Le mieux est de la charger ici avec get_font().
    
    def __init__(self, x, y, largeur, hauteur, texte, action_liee):
        """Initialise un bouton cliquable."""
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.texte = texte
        self.action_liee = action_liee
        
        # Utiliser les couleurs définies dans main_menu_content.py
        self.couleur_inactive = BUTTON_INACTIVE_COLOR
        self.couleur_active = BUTTON_ACTIVE_COLOR
        self.couleur = self.couleur_inactive
        self.est_survole = False
        
        # Charger la police (utilise la taille par défaut du menu)
        # Utilisation de None pour le path et la size pour utiliser les valeurs par défaut
        self.police = get_font(None, None)
        

    def draw(self, surface, gif_image=None): 
        """Dessine le bouton et gère l'état de survol."""
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if not self.est_survole: 
                self.SOUND_HOVER.play()
                self.est_survole = True
            self.couleur = self.couleur_active
        else:
            if self.est_survole: 
                self.est_survole = False
            self.couleur = self.couleur_inactive

        pygame.draw.rect(surface, self.couleur, self.rect)

        # Utilisation de COLORS['white'] au lieu de BLANC
        texte_surface = self.police.render(self.texte, True, COLORS['white']) 
        texte_rect = texte_surface.get_rect(center=self.rect.center)
        surface.blit(texte_surface, texte_rect)

    def manage_event(self, event):
        """
        Gère les événements liés au bouton (clic de souris).
        Joue un son au clic.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Clic gauche de la souris
                if self.rect.collidepoint(event.pos):
                    self.SOUND_CLICK.play() # Joue le son de clic
                    return self.action_liee
        return None
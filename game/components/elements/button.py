import pygame

from game.config import *
from game.components.button_style import BUTTON_ACTIVE_COLOR, BUTTON_INACTIVE_COLOR

class Button:
    # Sons partagés entre tous les boutons, chargés une seule fois
    # à la première instanciation (pas au chargement du module).
    _sounds_loaded = False
    SOUND_CLICK = None
    SOUND_HOVER = None

    # Police doit être chargée ici ou passée en paramètre.
    # Le mieux est de la charger ici avec get_font().

    def __init__(self, x, y, width, height, text, linked_action):
        """Initialise un bouton cliquable."""
        if not Button._sounds_loaded:
            pygame.mixer.init()
            Button.SOUND_CLICK = pygame.mixer.Sound(get_resource_path(join(AUDIO_DIR, 'sounds', 'yes_clicked.wav')))
            Button.SOUND_HOVER = pygame.mixer.Sound(get_resource_path(join(AUDIO_DIR, 'sounds', 'hover_click.wav')))
            Button._sounds_loaded = True

        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.linked_action = linked_action

        # Utiliser les couleurs définies dans main_menu_content.py
        self.inactive_color = BUTTON_INACTIVE_COLOR
        self.active_color = BUTTON_ACTIVE_COLOR
        self.color = self.inactive_color
        self.is_hovered = False

        # Charger la police (utilise la taille par défaut du menu)
        # Utilisation de None pour le path et la size pour utiliser les valeurs par défaut
        self.font = get_font(None, None)


    def draw(self, surface, gif_image=None):
        """Dessine le bouton et gère l'état de survol."""
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if not self.is_hovered:
                self.SOUND_HOVER.play()
                self.is_hovered = True
            self.color = self.active_color
        else:
            if self.is_hovered:
                self.is_hovered = False
            self.color = self.inactive_color

        pygame.draw.rect(surface, self.color, self.rect)

        # Utilisation de COLORS['white'] au lieu de BLANC
        text_surface = self.font.render(self.text, True, COLORS['white'])
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def manage_event(self, event):
        """
        Gère les événements liés au bouton (clic de souris).
        Joue un son au clic.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Clic gauche de la souris
                if self.rect.collidepoint(event.pos):
                    self.SOUND_CLICK.play() # Joue le son de clic
                    return self.linked_action
        return None
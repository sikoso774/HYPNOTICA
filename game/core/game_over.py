# Fichier: game/core/game_over.py
import pygame as pg
from ..config.settings import *
from ..config.utils import get_resource_path
from ..components.elements.textscroller import TextScroller
from .base_screen import BaseScreen # Import de la nouvelle classe mère

class GameOver(BaseScreen):
    def __init__(self, game):
        super().__init__(game) # Initialisation du parent
        self.music_name = 'game_over' # Le BaseScreen jouera ça automatiquement
        
        # --- Chargement spécifique ---
        self.scroller = TextScroller()
        self._load_background()

    def _load_background(self):
        bg_path = get_resource_path(join("assets", "images", "Game-Over-Wallpaper-48909.jpg"))
        try:
            self.background = pg.image.load(bg_path).convert()
            self.background = pg.transform.scale(self.background, (WIDTH, HEIGHT))
        except pg.error:
            self.background = pg.Surface((WIDTH, HEIGHT))
            self.background.fill(COLORS['black'])

    def on_event(self, event):
        # On surcharge uniquement la gestion des touches spécifiques
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                self.sound.stop_music()
                return "restart"
            elif event.key == pg.K_q:
                self.quit_game()
            elif event.key == pg.K_a:
                self.sound.stop_music()
                return "credits"
        return None

    def draw(self):
        # On définit juste ce qui s'affiche, la boucle est gérée par le parent
        self.screen.blit(self.background, (0, 0))
        self.scroller.draw_and_scroll(self.screen)


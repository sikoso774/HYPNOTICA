# Fichier: game/core/game_over.py
import pygame
from ..config.settings import *
from ..config.support import get_resource_path
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
            self.background = pygame.image.load(bg_path).convert()
            self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        except pygame.error:
            self.background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            self.background.fill(COLORS['black'])

    def on_event(self, event):
        # On surcharge uniquement la gestion des touches spécifiques
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.sound.stop_music()
                return "restart"
            elif event.key == pygame.K_q:
                self.quit_game()
            elif event.key == pygame.K_a:
                self.sound.stop_music()
                return "credits"
        return None

    def draw(self):
        # On définit juste ce qui s'affiche, la boucle est gérée par le parent
        self.screen.blit(self.background, (0, 0))
        self.scroller.draw_and_scroll(self.screen)

# Bloc de test indépendant
if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    game_over = GameOver(game=None)
    action = game_over.run()
    print(f"Action choisie : {action}")
    pygame.quit()
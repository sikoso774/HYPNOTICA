# Fichier: game/core/game_over.py
import pygame as pg
from game.config import *
from game.components import Button, BUTTON_WITDH, BUTTON_HEIGHT, BUTTON_SPACING
from game.core.screens import BaseScreen # Import de la nouvelle classe mère

class GameOver(BaseScreen):
    def __init__(self, game):
        super().__init__(game) # Initialisation du parent
        self.music_name = 'game_over' # Le BaseScreen jouera ça automatiquement

        # --- Chargement spécifique ---
        self._load_background()
        self._load_fonts()
        self._build_buttons()

    def _load_background(self):
        bg_path = get_resource_path(join("assets", "images", "Game-Over-Wallpaper-48909.jpg"))
        try:
            self.background = pg.image.load(bg_path).convert()
            self.background = pg.transform.scale(self.background, (WIDTH, HEIGHT))
        except pg.error:
            self.background = pg.Surface((WIDTH, HEIGHT))
            self.background.fill(COLORS['black'])

        # Voile semi-transparent pour garder le fond lisible sous le texte/boutons
        self.overlay = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        self.overlay.fill((0, 0, 0, 225))

    def _load_fonts(self):
        self.font_title = get_font(DEFAULT_FONT_NAME, 64)

    def _build_buttons(self):
        center_x = WIDTH // 2 - BUTTON_WITDH // 2
        start_y = HEIGHT // 2 - BUTTON_HEIGHT // 2

        self.buttons = [
            Button(center_x, start_y, BUTTON_WITDH, BUTTON_HEIGHT,
                   "REJOUER", "game"),
            Button(center_x, start_y + (BUTTON_HEIGHT + BUTTON_SPACING),
                   BUTTON_WITDH, BUTTON_HEIGHT, "CREDITS", "credits"),
            Button(center_x, start_y + (BUTTON_HEIGHT + BUTTON_SPACING) * 2,
                   BUTTON_WITDH, BUTTON_HEIGHT, "QUITTER", "quit"),
        ]

    def on_event(self, event):
        # Boutons cliquables (souris)
        for button in self.buttons:
            action = button.manage_event(event)
            if action:
                self.sound.play_sfx('click')
                if action == 'quit':
                    self.quit_game()
                self.sound.stop_music()
                return action

        # Raccourcis clavier équivalents
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                self.sound.stop_music()
                return "game"
            elif event.key == pg.K_a:
                self.sound.stop_music()
                return "credits"
            elif event.key == pg.K_q:
                self.quit_game()
        return None

    def draw(self):
        # 1. Fond assombri pour garantir la lisibilité
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.overlay, (0, 0))

        # 2. Titre
        title_surf = self.font_title.render("GAME OVER", True, COLORS['white'])
        title_rect = title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        self.screen.blit(title_surf, title_rect)

        # 3. Boutons
        for button in self.buttons:
            button.draw(self.screen)


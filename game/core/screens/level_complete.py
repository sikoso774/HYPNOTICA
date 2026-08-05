import pygame as pg
from game.config import *
from game.components import Button, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_SPACING
from game.core.screens import BaseScreen

RING_COLOR = (26, 20, 38)
SUBTITLE_COLOR = (144, 131, 171)


class LevelComplete(BaseScreen):
    """Shown when the player reaches the exit marker before the timer runs out."""

    def __init__(self, game):
        super().__init__(game)
        self.music_name = 'credits'  # No dedicated victory track yet; reuse an existing one

        self._load_fonts()
        self._build_buttons()

    def _load_fonts(self):
        self.font_title = get_font(DEFAULT_FONT_NAME, 56)
        self.font_subtitle = get_font(BODY_FONT_NAME, 20)

    def _build_buttons(self):
        center_x = WIDTH // 2 - BUTTON_WIDTH // 2
        start_y = HEIGHT // 2 - BUTTON_HEIGHT // 2

        self.buttons = [
            Button(center_x, start_y, BUTTON_WIDTH, BUTTON_HEIGHT,
                   "REJOUER", "game"),
            Button(center_x, start_y + (BUTTON_HEIGHT + BUTTON_SPACING),
                   BUTTON_WIDTH, BUTTON_HEIGHT, "CARTE DES PROFONDEURS", "world_map"),
            Button(center_x, start_y + (BUTTON_HEIGHT + BUTTON_SPACING) * 2,
                   BUTTON_WIDTH, BUTTON_HEIGHT, "QUITTER", "quit"),
        ]

    def on_event(self, event):
        for button in self.buttons:
            action = button.manage_event(event)
            if action:
                self.sound.play_sfx('click')
                if action == 'quit':
                    self.quit_game()
                self.sound.stop_music()
                return action

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                self.sound.stop_music()
                return "game"
            elif event.key == pg.K_m:
                self.sound.stop_music()
                return "world_map"
            elif event.key == pg.K_q:
                self.quit_game()
        return None

    def draw(self):
        self.screen.fill(COLORS['black'])
        self._draw_background_rings()

        title_surf = self.font_title.render("PASSAGE FRANCHI", True, COLORS['green'])
        title_rect = title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        self.screen.blit(title_surf, title_rect)

        subtitle_surf = self.font_subtitle.render("La premiere porte s'est refermee derriere toi.",
                                                    True, SUBTITLE_COLOR)
        subtitle_rect = subtitle_surf.get_rect(center=(WIDTH // 2, HEIGHT // 4 + 55))
        self.screen.blit(subtitle_surf, subtitle_rect)

        for button in self.buttons:
            button.draw(self.screen)

    def _draw_background_rings(self):
        center = (WIDTH // 2, HEIGHT // 2)
        for radius in (220, 340, 460):
            pg.draw.circle(self.screen, RING_COLOR, center, radius, 1)

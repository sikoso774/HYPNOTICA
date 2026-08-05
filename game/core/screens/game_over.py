# File: game/core/game_over.py
import pygame as pg
from game.config import *
from game.components import Button, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_SPACING
from game.core.screens import BaseScreen # Import of the new parent class

# Death flavor text, keyed by Game.game_over_reason (set by Level3D)
REASON_TEXT = {
    'caught': "Elle t'a trouve dans le noir.",
    'timeout': "Le temps s'est ecoule.",
}


class GameOver(BaseScreen):
    """The game-over screen, shown when the level timer runs out."""

    def __init__(self, game):
        super().__init__(game) # Parent initialization
        self.music_name = 'game_over' # BaseScreen will play this automatically

        # --- Screen-specific loading ---
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

        # Semi-transparent overlay to keep the background readable under the text/buttons
        self.overlay = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        self.overlay.fill((0, 0, 0, 225))

    def _load_fonts(self):
        self.font_title = get_font(DEFAULT_FONT_NAME, 64)
        self.font_subtitle = get_font(BODY_FONT_NAME, 20)

    def _build_buttons(self):
        center_x = WIDTH // 2 - BUTTON_WIDTH // 2
        start_y = HEIGHT // 2 - BUTTON_HEIGHT // 2

        self.buttons = [
            Button(center_x, start_y, BUTTON_WIDTH, BUTTON_HEIGHT,
                   "REJOUER", "game"),
            Button(center_x, start_y + (BUTTON_HEIGHT + BUTTON_SPACING),
                   BUTTON_WIDTH, BUTTON_HEIGHT, "CREDITS", "credits"),
            Button(center_x, start_y + (BUTTON_HEIGHT + BUTTON_SPACING) * 2,
                   BUTTON_WIDTH, BUTTON_HEIGHT, "QUITTER", "quit"),
        ]

    def on_event(self, event):
        # Clickable buttons (mouse)
        for button in self.buttons:
            action = button.manage_event(event)
            if action:
                self.sound.play_sfx('click')
                if action == 'quit':
                    self.quit_game()
                self.sound.stop_music()
                return action

        # Equivalent keyboard shortcuts
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
        # 1. Darkened background to ensure readability
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.overlay, (0, 0))

        # 2. Title
        title_surf = self.font_title.render("GAME OVER", True, COLORS['white'])
        title_rect = title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        self.screen.blit(title_surf, title_rect)

        reason = getattr(self.game, 'game_over_reason', 'timeout')
        subtitle_surf = self.font_subtitle.render(REASON_TEXT.get(reason, REASON_TEXT['timeout']),
                                                    True, (144, 131, 171))
        subtitle_rect = subtitle_surf.get_rect(center=(WIDTH // 2, HEIGHT // 4 + 55))
        self.screen.blit(subtitle_surf, subtitle_rect)

        # 3. Buttons
        for button in self.buttons:
            button.draw(self.screen)


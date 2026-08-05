import math
import pygame as pg
from game.config.settings import *
from game.components import *
from .base_screen import BaseScreen  # Import of the parent class

# Menu button configuration (Text, Action, Y position)
START_Y = HEIGHT // 2 - 50
BUTTONS_MENU = [
    {'text': 'JOUER', 'action': 'world_map', 'y_offset': START_Y},
    {'text': 'INSTRUCTIONS', 'action': 'instructions', 'y_offset': START_Y + (BUTTON_HEIGHT + BUTTON_SPACING)},
    {'text': 'CREDITS', 'action': 'credits', 'y_offset': START_Y + (BUTTON_HEIGHT + BUTTON_SPACING) * 2},
    {'text': 'QUITTER', 'action': 'quit', 'y_offset': START_Y + (BUTTON_HEIGHT + BUTTON_SPACING) * 3},
]

TITLE_PANEL_BG = (21, 15, 36)
TITLE_PANEL_BORDER = (74, 63, 92)
SUBTITLE_COLOR = (144, 131, 171)

OVERLAY_BASE_ALPHA = 130
OVERLAY_PULSE_AMPLITUDE = 12
OVERLAY_PULSE_SPEED = 0.0006

CURSOR_COLOR = COLORS['green']
CURSOR_RADIUS = 6


class MainMenu(BaseScreen):
    """The main menu screen, with an animated GIF background and navigation buttons."""

    def __init__(self, game):
        super().__init__(game)
        self.music_name = 'menu'  # Reference to the key in SoundHandler

        # 1. Assets (GIF)
        gif_path = get_resource_path(join(IMAGES_DIR, "hypnose_frames"))
        self.gif_animator = AnimationGif(gif_path, self.screen)

        # 2. Fonts
        self.font_title = get_font(DEFAULT_FONT_NAME, 52)
        self.font_subtitle = get_font(BODY_FONT_NAME, 18)

        # 3. Buttons
        self.buttons = []
        # Center the buttons relative to the screen width
        center_x = self.screen.get_width() // 2 - BUTTON_WIDTH // 2

        for button_data in BUTTONS_MENU:
            self.buttons.append(
                Button(center_x, button_data['y_offset'], BUTTON_WIDTH, BUTTON_HEIGHT,
                       button_data['text'], button_data['action'])
            )

    def run(self):
        pg.mouse.set_visible(False)
        try:
            return super().run()
        finally:
            pg.mouse.set_visible(True)

    def on_event(self, event):
        # Handle button clicks
        for button in self.buttons:
            action = button.manage_event(event)
            if action:
                self.sound.play_sfx('click') # Little bonus: click sound!
                return action

        # Keyboard shortcut (Q to quit)
        if event.type == pg.KEYDOWN and event.key == pg.K_q:
            self.quit_game()

        return None

    def update(self):
        # Update the GIF animation every frame
        self.gif_animator.animate()

    def draw(self):
        # 1. Background (GIF)
        frame_index = self.gif_animator.animation_frame
        self.screen.blit(self.gif_animator.frames[frame_index], (0, 0))

        # 2. Dim overlay: the spiral is far higher-contrast than the rest of the
        # game, this calms it down so foreground text/buttons stay legible.
        self._draw_dim_overlay()

        # 3. Title block (on its own translucent panel, so it reads regardless
        # of what the spiral is doing behind it)
        self._draw_title_block()

        # 4. Buttons
        for button in self.buttons:
            button.draw(self.screen, self.gif_animator.frames[frame_index])

        self._draw_cursor()

    def _draw_dim_overlay(self):
        pulse = math.sin(pg.time.get_ticks() * OVERLAY_PULSE_SPEED) * OVERLAY_PULSE_AMPLITUDE
        alpha = max(0, min(255, int(OVERLAY_BASE_ALPHA + pulse)))
        overlay = pg.Surface(self.screen.get_size(), pg.SRCALPHA)
        overlay.fill((0, 0, 0, alpha))
        self.screen.blit(overlay, (0, 0))

    def _draw_title_block(self):
        title_surf = self.font_title.render("HYPNOTICA", True, COLORS['white'])
        subtitle_surf = self.font_subtitle.render("Zoléni KOKOLO ZASSI - 2025", True, SUBTITLE_COLOR)

        panel_w = max(title_surf.get_width(), subtitle_surf.get_width()) + 80
        panel_rect = pg.Rect(0, 0, panel_w, 110)
        panel_rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 4 + 10)

        panel_surf = pg.Surface(panel_rect.size, pg.SRCALPHA)
        panel_surf.fill((*TITLE_PANEL_BG, 210))
        pg.draw.rect(panel_surf, TITLE_PANEL_BORDER, panel_surf.get_rect(), 1)
        self.screen.blit(panel_surf, panel_rect)

        title_rect = title_surf.get_rect(center=(panel_rect.centerx, panel_rect.top + 38))
        self.screen.blit(title_surf, title_rect)

        subtitle_rect = subtitle_surf.get_rect(center=(panel_rect.centerx, panel_rect.top + 78))
        self.screen.blit(subtitle_surf, subtitle_rect)

    def _draw_cursor(self):
        """Custom crosshair cursor, drawn in place of the OS arrow to fit the theme."""
        x, y = pg.mouse.get_pos()
        pg.draw.circle(self.screen, CURSOR_COLOR, (x, y), CURSOR_RADIUS, 1)
        pg.draw.line(self.screen, CURSOR_COLOR, (x - CURSOR_RADIUS - 4, y), (x - 2, y), 1)
        pg.draw.line(self.screen, CURSOR_COLOR, (x + 2, y), (x + CURSOR_RADIUS + 4, y), 1)
        pg.draw.line(self.screen, CURSOR_COLOR, (x, y - CURSOR_RADIUS - 4), (x, y - 2), 1)
        pg.draw.line(self.screen, CURSOR_COLOR, (x, y + 2), (x, y + CURSOR_RADIUS + 4), 1)

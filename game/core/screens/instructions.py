import pygame as pg
from game.config import *
from .base_screen import BaseScreen

# Instructions content, matching the current raycasting controls (game/raycasting_engine/player.py)
# and the 60s survival timer (game/core/levels/level_3d.py) - no win condition is coded yet.
INSTRUCTIONS_CONTENT = [
    {'type': 'title', 'value': "INSTRUCTIONS"},
    {'type': 'spacer', 'height': 20},
    {'type': 'label', 'value': "DEPLACEMENT"},
    {'type': 'text', 'value': "Z / W  -  Avancer"},
    {'type': 'text', 'value': "S  -  Reculer"},
    {'type': 'text', 'value': "Q / A  -  Strafe gauche"},
    {'type': 'text', 'value': "D  -  Strafe droite"},
    {'type': 'text', 'value': "Fleches GAUCHE / DROITE  -  Tourner la camera"},
    {'type': 'spacer', 'height': 16},
    {'type': 'label', 'value': "OBJECTIF"},
    {'type': 'text', 'value': "Explore la profondeur avant la fin du temps."},
    {'type': 'dim', 'value': "Chaque seconde compte."},
    {'type': 'spacer', 'height': 20},
    {'type': 'hint', 'value': "ESPACE - Continuer"},
]

PANEL_BG = (21, 15, 36)
PANEL_BORDER = (74, 63, 92)
LABEL_COLOR = COLORS['green']
DIM_TEXT_COLOR = (144, 131, 171)
RING_COLOR = (26, 20, 38)
PANEL_PADDING_X = 90
PANEL_PADDING_Y = 22


class Instructions(BaseScreen):
    """The instructions screen, with a typewriter-style text reveal animation."""

    def __init__(self, game):
        super().__init__(game)
        self.instruction_data = INSTRUCTIONS_CONTENT

        # Animation variables
        self.current_char_index = 0
        self.last_char_time = 0
        self.typing_speed = 30
        self.total_chars = 0

        self.prepared_items = []
        self._prepare_content()
        self._compute_panel_rect()

        # Reset for the animation on startup
        self.last_char_time = pg.time.get_ticks()

    def _prepare_content(self):
        current_y = HEIGHT // 10
        self.total_chars = 0

        style_by_type = {
            'title': (DEFAULT_FONT_NAME, 40, COLORS['white']),
            'label': (BODY_FONT_BOLD_NAME, 20, LABEL_COLOR),
            'text': (BODY_FONT_NAME, 20, COLORS['white']),
            'dim': (BODY_FONT_NAME, 16, DIM_TEXT_COLOR),
            'hint': (BODY_FONT_NAME, 16, DIM_TEXT_COLOR),
        }

        for item in self.instruction_data:
            if item['type'] == 'spacer':
                current_y += item.get('height', 20)
                continue

            font_path, size, color = style_by_type[item['type']]
            font = get_font(font_path, size)

            self.prepared_items.append({
                'full_text': item['value'],
                'font': font,
                'color': color,
                'y': current_y,
                'start_index': self.total_chars,
                'length': len(item['value']),
            })
            self.total_chars += len(item['value'])
            current_y += font.get_height() + 6

    def _compute_panel_rect(self):
        if not self.prepared_items:
            self.panel_rect = pg.Rect(0, 0, 0, 0)
            return

        max_width = max(item['font'].size(item['full_text'])[0] for item in self.prepared_items)
        top = self.prepared_items[0]['y'] - self.prepared_items[0]['font'].get_height() // 2
        last = self.prepared_items[-1]
        bottom = last['y'] + last['font'].get_height() // 2

        self.panel_rect = pg.Rect(0, 0, max_width + PANEL_PADDING_X * 2, (bottom - top) + PANEL_PADDING_Y * 2)
        self.panel_rect.center = (WIDTH // 2, (top + bottom) // 2)

    def on_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                # If the animation isn't finished, speed it up
                if self.current_char_index < self.total_chars:
                    self.current_char_index = self.total_chars
                else:
                    return "menu"
        return None

    def update(self):
        current_time = pg.time.get_ticks()
        if self.current_char_index < self.total_chars:
            if current_time - self.last_char_time > self.typing_speed:
                self.current_char_index += 1
                self.last_char_time = current_time

    def draw(self):
        self.screen.fill(COLORS['black'])
        self._draw_background_rings()

        panel_surf = pg.Surface(self.panel_rect.size, pg.SRCALPHA)
        panel_surf.fill((*PANEL_BG, 210))
        pg.draw.rect(panel_surf, PANEL_BORDER, panel_surf.get_rect(), 1)
        self.screen.blit(panel_surf, self.panel_rect)

        for item in self.prepared_items:
            # Only display once the global index has passed this line's start_index
            if self.current_char_index > item['start_index']:
                # How many characters of this line should be displayed?
                char_limit = min(self.current_char_index - item['start_index'], item['length'])
                text_to_render = item['full_text'][:char_limit]

                surf = item['font'].render(text_to_render, True, item['color'])
                rect = surf.get_rect(center=(WIDTH // 2, item['y']))
                self.screen.blit(surf, rect)

    def _draw_background_rings(self):
        center = (WIDTH // 2, HEIGHT // 2)
        for radius in (260, 340):
            pg.draw.circle(self.screen, RING_COLOR, center, radius, 1)

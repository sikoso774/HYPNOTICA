import pygame as pg
from game.config import *
from .base_screen import BaseScreen

# Credits content
PURPLE = COLORS['purple']
DIM_TEXT_COLOR = (144, 131, 171)
RING_COLOR = (40, 20, 64)
IMAGE_PATH = get_resource_path(join(IMAGES_DIR, "Zoléni_Cyberpunk.jpg"))

CREDITS_CONTENT = [
    {'type': 'title', 'value': "CREDITS"},
    {'type': 'spacer', 'height': 70},

    {'type': 'header', 'value': "Developpeur"},
    {'type': 'text', 'value': "Sikoso 774"},
    {'type': 'spacer', 'height': 30},
    {'type': 'image', 'value': "developer_image", 'image_path': IMAGE_PATH, 'image_scale_factor': 0.42},
    {'type': 'spacer', 'height': 60},

    {'type': 'header', 'value': "Musiques"},
    {'type': 'text', 'value': "waera - harinezumi [NCS Release]"},
    {'type': 'dim', 'value': "Licensed under Creative Commons"},
    {'type': 'spacer', 'height': 26},
    {'type': 'text', 'value': "Max Brhon - AI [NCS Release]"},
    {'type': 'dim', 'value': "Licensed under Creative Commons"},
    {'type': 'spacer', 'height': 26},
    {'type': 'text', 'value': "More Plastic - Rewind [NCS Release]"},
    {'type': 'dim', 'value': "Licensed under Creative Commons"},
    {'type': 'spacer', 'height': 60},

    {'type': 'highlight', 'value': "Concept & Univers : HYPNOTICA"},
    {'type': 'spacer', 'height': 60},

    {'type': 'header', 'value': "Remerciements"},
    {'type': 'text', 'value': "Ma famille et mes proches"},
    {'type': 'text', 'value': "La communaute Pygame"},
    {'type': 'spacer', 'height': 80},

    {'type': 'glow', 'value': "Merci d'avoir joue.", 'color': COLORS['green']},
    {'type': 'spacer', 'height': 160},
]


class Credits(BaseScreen):
    """The scrolling end-credits screen."""

    def __init__(self, game):
        super().__init__(game)
        self.music_name = 'credits'

        self.credit_data = CREDITS_CONTENT
        self.scrolling_speed = 1.5

        self._build_fade_mask()

        # Content preparation
        self.prepare_credits = self._prepare_credits()

        # Height calculation
        _, self.screen_h = self.screen.get_size()
        self.total_height = sum(item['height'] for item in self.prepare_credits) + self.screen_h * 0.1

        # Variable initialization (will be reset in run)
        self.credits_y = self.screen_h

    def run(self):
        """Puts the text back at the bottom of the screen before starting the loop."""
        self.credits_y = self.screen_h
        return super().run()

    # --- Fade mask (top/bottom edges dissolve into black, like real end credits) ---

    def _build_fade_mask(self):
        fade_height = 100
        mask = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        mask.fill((255, 255, 255, 255))
        for y in range(fade_height):
            alpha = int(255 * (y / fade_height))
            pg.draw.line(mask, (255, 255, 255, alpha), (0, y), (WIDTH, y))
            pg.draw.line(mask, (255, 255, 255, alpha), (0, HEIGHT - 1 - y), (WIDTH, HEIGHT - 1 - y))
        self.fade_mask = mask

    # --- Content preparation ---

    def _load_images(self) -> dict:
        loaded_images = {}
        for item in CREDITS_CONTENT:
            if item['type'] == 'image' and 'image_path' in item:
                try:
                    img = pg.image.load(item['image_path']).convert_alpha()
                    scaled_width = int(WIDTH * item.get('image_scale_factor', 1))
                    scaled_height = int(HEIGHT * item.get('image_scale_factor', 1))
                    img = pg.transform.scale(img, (scaled_width, scaled_height))
                    loaded_images[item['value']] = self._make_portrait(img)
                except pg.error:
                    loaded_images[item['value']] = pg.Surface((1, 1), pg.SRCALPHA)
        return loaded_images

    def _make_portrait(self, image):
        """Center-crops the image to a circle with a soft purple glow ring."""
        w, h = image.get_size()
        side = min(w, h)
        crop_rect = pg.Rect(0, 0, side, side)
        crop_rect.center = (w // 2, h // 2)
        square = image.subsurface(crop_rect).copy()

        circle_mask = pg.Surface((side, side), pg.SRCALPHA)
        pg.draw.circle(circle_mask, (255, 255, 255, 255), (side // 2, side // 2), side // 2)
        portrait = square.copy()
        portrait.blit(circle_mask, (0, 0), special_flags=pg.BLEND_RGBA_MULT)

        margin = 16
        framed = pg.Surface((side + margin * 2, side + margin * 2), pg.SRCALPHA)
        center = framed.get_rect().center
        for radius_offset, alpha in ((12, 22), (8, 40), (4, 65)):
            pg.draw.circle(framed, (*PURPLE, alpha), center, side // 2 + radius_offset)
        framed.blit(portrait, portrait.get_rect(center=center))
        pg.draw.circle(framed, PURPLE, center, side // 2 + 2, width=3)
        return framed

    def _render_glow_text(self, font, text, fg_color, glow_color=PURPLE, glow_alpha=90):
        base = font.render(text, True, fg_color)
        pad = 14
        surf = pg.Surface((base.get_width() + pad * 2, base.get_height() + pad * 2), pg.SRCALPHA)
        center = surf.get_rect().center

        glow_surf = font.render(text, True, glow_color)
        glow_surf.set_alpha(glow_alpha)
        for dx, dy in ((3, 0), (-3, 0), (0, 3), (0, -3), (2, 2), (-2, -2), (2, -2), (-2, 2)):
            surf.blit(glow_surf, glow_surf.get_rect(center=(center[0] + dx, center[1] + dy)))

        surf.blit(base, base.get_rect(center=center))
        return surf

    def _prepare_credits(self):
        prepared_list = []
        loaded_images = self._load_images()

        style_by_type = {
            'header': (BODY_FONT_BOLD_NAME, 24, PURPLE),
            'text': (BODY_FONT_NAME, 20, COLORS['white']),
            'dim': (BODY_FONT_NAME, 15, DIM_TEXT_COLOR),
            'highlight': (BODY_FONT_BOLD_NAME, 22, PURPLE),
        }

        for item in self.credit_data:
            prepared_item = {'type': item['type']}

            if item['type'] == 'title':
                font = get_font(DEFAULT_FONT_NAME, 60)
                prepared_item['surface'] = self._render_glow_text(font, item['value'], COLORS['white'])
                prepared_item['height'] = prepared_item['surface'].get_height() * 1.2

            elif item['type'] == 'glow':
                font = get_font(DEFAULT_FONT_NAME, 36)
                color = item.get('color', PURPLE)
                prepared_item['surface'] = self._render_glow_text(font, item['value'], color, glow_color=color)
                prepared_item['height'] = prepared_item['surface'].get_height() * 1.4

            elif item['type'] in style_by_type:
                font_path, size, color = style_by_type[item['type']]
                font = get_font(font_path, size)
                text_surf = font.render(item['value'], True, color)
                prepared_item['surface'] = text_surf
                prepared_item['height'] = text_surf.get_height() * 1.5

            elif item['type'] == 'image':
                image = loaded_images.get(item['value'])
                if image:
                    prepared_item['surface'] = image
                    prepared_item['height'] = image.get_height() + 20
                else:
                    prepared_item['surface'] = pg.Surface((1, 1), pg.SRCALPHA)
                    prepared_item['height'] = 0

            elif item['type'] == 'spacer':
                prepared_item['height'] = item.get('height', 0)

            prepared_list.append(prepared_item)
        return prepared_list

    def on_event(self, event):
        if event.type == pg.KEYDOWN:
            # M key to return to the menu
            if event.key == pg.K_m:
                self.sound.play_sfx('click')
                return "menu"
            elif event.key == pg.K_q:
                self.quit_game()
        return None

    def update(self):
        self.credits_y -= self.scrolling_speed
        # Once everything has scrolled past, loop back to the bottom
        if self.credits_y < -self.total_height:
            self.credits_y = self.screen_h

    def draw(self):
        self.screen.fill(COLORS['black'])
        self._draw_background()

        center_x = self.screen.get_width() // 2
        content_surf = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        y_offset = self.credits_y

        for item in self.prepare_credits:
            if item['type'] != 'spacer':
                surf = item['surface']
                rect = surf.get_rect(center=(center_x, y_offset + surf.get_height() // 2))
                content_surf.blit(surf, rect)
            y_offset += item['height']

        content_surf.blit(self.fade_mask, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
        self.screen.blit(content_surf, (0, 0))

        self._draw_hints()

    def _draw_background(self):
        center = (WIDTH // 2, HEIGHT // 2)
        for radius in (200, 320, 440):
            pg.draw.circle(self.screen, RING_COLOR, center, radius, 1)

    def _draw_hints(self):
        hint_text = "Q : quitter   M : retour au menu"
        font = get_font(BODY_FONT_NAME, 14)
        surf = font.render(hint_text, True, DIM_TEXT_COLOR)
        rect = surf.get_rect(center=(WIDTH // 2, HEIGHT - 18))
        self.screen.blit(surf, rect)

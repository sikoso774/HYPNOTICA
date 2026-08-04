import pygame as pg
from game.config import *


class TextScroller:
    """Scrolls a fixed list of text lines horizontally across the screen."""

    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT

        # Load the font
        self.font = get_font(DEFAULT_FONT_NAME, 24)

        # List of text to display
        self.text_list = [
            "GAME OVER",
            "",
            "Press R to Replay",
            "",
            "Press A for Credits",
            "",
            "Press Q to Quit",
        ]

        self.x = self.width # Starts off-screen on the right
        self.speed = 1 # Scroll speed

    def draw_and_scroll(self, surface):
        """
        Draws and scrolls the text.
        """
        max_text_width = 0

        for i, line in enumerate(self.text_list):
            # Render the text (GREEN color -> COLORS['green'])
            text_surf = self.font.render(line, True, COLORS['green'])

            # Positioning
            # Centered vertically a bit lower + offset per line
            text_rect = text_surf.get_rect(y=self.height // 9.5 + i * 30)
            text_rect.x = self.x

            surface.blit(text_surf, text_rect)

            # Track the widest line to know when to reset the loop
            if text_rect.width > max_text_width:
                max_text_width = text_rect.width

        # Update the position
        self.x -= self.speed

        # Reset the position once all the text has scrolled off-screen
        if self.x < -max_text_width:
            self.x = self.width
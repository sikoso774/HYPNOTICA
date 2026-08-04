import math

import pygame

from game.config import *
from game.components.button_style import (
    BUTTON_RADIUS, BUTTON_BG, BUTTON_BG_ALPHA, BUTTON_BORDER_COLOR,
    BUTTON_BORDER_HOVER_COLOR, BUTTON_TEXT_COLOR,
    BUTTON_GLOW_PULSE_AMPLITUDE, BUTTON_GLOW_PULSE_SPEED,
)


class Button:
    """A clickable UI button with hover/click sound feedback."""

    # Sounds shared between all buttons, loaded only once
    # on first instantiation (not at module load time).
    _sounds_loaded = False
    SOUND_CLICK = None
    SOUND_HOVER = None

    # Font must be loaded here or passed as a parameter.
    # Best is to load it here with get_font().

    def __init__(self, x, y, width, height, text, linked_action):
        """Initializes a clickable button."""
        if not Button._sounds_loaded:
            pygame.mixer.init()
            Button.SOUND_CLICK = pygame.mixer.Sound(get_resource_path(join(AUDIO_DIR, 'sounds', 'yes_clicked.wav')))
            Button.SOUND_HOVER = pygame.mixer.Sound(get_resource_path(join(AUDIO_DIR, 'sounds', 'hover_click.wav')))
            Button._sounds_loaded = True

        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.linked_action = linked_action
        self.is_hovered = False

        # Load the font (uses the menu's default size)
        # Passing None for path and size to fall back to the defaults
        self.font = get_font(None, None)

    def draw(self, surface, gif_image=None):
        """Draws the button as a translucent glass panel and handles the hover state."""
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if not self.is_hovered:
                self.SOUND_HOVER.play()
                self.is_hovered = True
        else:
            if self.is_hovered:
                self.is_hovered = False

        panel = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        pygame.draw.rect(panel, (*BUTTON_BG, BUTTON_BG_ALPHA), panel.get_rect(), border_radius=BUTTON_RADIUS)
        surface.blit(panel, self.rect)

        if self.is_hovered:
            pulse = math.sin(pygame.time.get_ticks() * BUTTON_GLOW_PULSE_SPEED) * BUTTON_GLOW_PULSE_AMPLITUDE
            border_width = 2
            border_color = BUTTON_BORDER_HOVER_COLOR
            glow_rect = self.rect.inflate(6 + pulse, 6 + pulse)
            glow = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
            pygame.draw.rect(glow, (*BUTTON_BORDER_HOVER_COLOR, 60), glow.get_rect(), border_radius=BUTTON_RADIUS + 3)
            surface.blit(glow, glow_rect)
        else:
            border_width = 1
            border_color = BUTTON_BORDER_COLOR

        pygame.draw.rect(surface, border_color, self.rect, border_width, border_radius=BUTTON_RADIUS)

        text_surface = self.font.render(self.text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def manage_event(self, event):
        """
        Handles events related to the button (mouse click).
        Plays a sound on click.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left mouse click
                if self.rect.collidepoint(event.pos):
                    self.SOUND_CLICK.play() # Plays the click sound
                    return self.linked_action
        return None
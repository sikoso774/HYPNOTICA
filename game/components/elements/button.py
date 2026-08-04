import pygame

from game.config import *
from game.components.button_style import BUTTON_ACTIVE_COLOR, BUTTON_INACTIVE_COLOR


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

        # Use the colors defined in main_menu_content.py
        self.inactive_color = BUTTON_INACTIVE_COLOR
        self.active_color = BUTTON_ACTIVE_COLOR
        self.color = self.inactive_color
        self.is_hovered = False

        # Load the font (uses the menu's default size)
        # Passing None for path and size to fall back to the defaults
        self.font = get_font(None, None)


    def draw(self, surface, gif_image=None):
        """Draws the button and handles the hover state."""
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if not self.is_hovered:
                self.SOUND_HOVER.play()
                self.is_hovered = True
            self.color = self.active_color
        else:
            if self.is_hovered:
                self.is_hovered = False
            self.color = self.inactive_color

        pygame.draw.rect(surface, self.color, self.rect)

        # Using COLORS['white'] instead of BLANC
        text_surface = self.font.render(self.text, True, COLORS['white'])
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
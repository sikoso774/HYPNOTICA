import os
import sys
import pygame as pg
from .settings import *

# Cache for storing font objects
_font_cache = {}

def get_resource_path(relative_path):
    """
    Returns the absolute path of a resource, compatible with PyInstaller
    (if the exe is built) and standard development.
    """
    try:
        # PyInstaller creates a temporary folder and stores the path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def get_font(font_path, size):
    """Loads or retrieves a font from a cache."""
    # ... (the font caching logic is moved/reused here)
    final_font_path = font_path if font_path is not None else DEFAULT_FONT_NAME
    final_font_size = size if size is not None else 25
    font_key = (final_font_path, final_font_size)

    if font_key not in _font_cache:
        try:
            abs_font_path = get_resource_path(final_font_path)
            _font_cache[font_key] = pg.font.Font(abs_font_path, final_font_size)
        except Exception as e:
            print(f"Error loading font: {e}")
            _font_cache[font_key] = pg.font.SysFont(None, final_font_size)

    return _font_cache[font_key]


def display_text_center(surface, text, color, y, font_path=None, font_size=None):
    """
    Displays horizontally centered text on the screen.
    """
    # Using the new caching function
    font = get_font(font_path, font_size)

    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=(WIDTH // 2, y))
    surface.blit(text_surf, text_rect)
import os
import sys
import pygame as pg
from .settings import * 

# Cache pour stocker les objets police
_font_cache = {}

def get_resource_path(relative_path):
    """
    Retourne le chemin absolu d'une ressource, compatible avec PyInstaller 
    (si l'exe est compilé) et le développement standard.
    """
    try:
        # PyInstaller crée un dossier temporaire et stocke le chemin dans _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def get_font(font_path, size):
    """Charge ou récupère une police depuis un cache."""
    # ... (Le contenu de la fonction de cache de police est déplacé/réutilisé ici)
    final_font_path = font_path if font_path is not None else DEFAULT_FONT_NAME
    final_font_size = size if size is not None else 25
    font_key = (final_font_path, final_font_size)

    if font_key not in _font_cache:
        try:
            abs_font_path = get_resource_path(final_font_path)
            _font_cache[font_key] = pg.font.Font(abs_font_path, final_font_size)
        except Exception as e:
            print(f"Erreur de chargement de la police: {e}")
            _font_cache[font_key] = pg.font.SysFont(None, final_font_size) 

    return _font_cache[font_key]


def display_text_center(surface, text, color, y, font_path=None, font_size=None):
    """
    Affiche du texte centré horizontalement sur l'écran.
    """
    # Utilisation de la nouvelle fonction de cache
    police_font = get_font(font_path, font_size)

    text_surf = police_font.render(text, True, color)
    texte_rect = text_surf.get_rect(center=(WIDTH // 2, y))
    surface.blit(text_surf, texte_rect)
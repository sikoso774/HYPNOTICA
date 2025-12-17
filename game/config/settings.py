# Fichier: game/config/settings.py
import os
from os.path import join

# --- Configuration Fenêtre ---
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
GAME_TITLE = "Deep Hypnotica"

# --- Chemins et Ressources ---
# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ASSETS_DIR = os.path.join("assets")
AUDIO_DIR = os.path.join(ASSETS_DIR, "audio")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")

DEFAULT_FONT_NAME = os.path.join(FONTS_DIR, "MINDCONTROL.ttf")

# --- Couleurs (Palette Globale) ---
# global colors palette
COLORS = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'gray': (100, 100, 100),
    
    # RGB
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    
    # Secondary solors
    'cyan': (0, 255, 255),
    'magenta': (255, 0, 255),
    'yellow': (255, 255, 0),
    
    # Others colors
    'dark_gray': (50, 50, 50),
    'orange': (181, 83, 38),
    'purple': (127, 0, 255),
    
    # Personal colors
    'ui_text': (255, 255, 255),
    'ui_hover': (200, 200, 200),
}

# --- Gameplay & Physique (Ex-gameplay_const.py) ---
PLAYER_SIZE = 50 
PLAYER_SPEED = 300
PHONE_SIZE = 30 
PHONE_SPEED = 120
GRAVITY = 9.8
JUMP_STRENGTH = -15
SATIETY_DECREASE_RATE = 10  # Vitesse de baisse de la faim
SATIETY_MAX = 10

# Player settings
PLAYER_SPRITE_PATH = None 
PHONE_SPRITE_PATH = None 

# Satiety settings
SATIETY_START = 100.0
SATIETY_DECREASE_RATE = 0.05
SATIETY_INCREASE_AMOUNT = 10

# Sons des boutons (doivent être traités par audio_importer)
SOUND_CLICK_FILE = 'yes_clicked'  # Nom du fichier sans extension
SOUND_HOVER_FILE = 'hover_click' # Nom du fichier sans extension
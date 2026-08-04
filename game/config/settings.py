# Fichier: game/config/settings.py
import os
import math
from os.path import join

# --- Configuration Fenêtre ---
WIDTH = 800# (800 + 220)
HEIGHT = 600
FPS = 60
GAME_TITLE = "Hypnotica"

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

# --- Gameplay & Physique  ---
GRAVITY = 0.8
JUMP_STRENGTH = -15

# Player settings
PLAYER_DATA = {
    'size': 50,
    'speed': 300,
    'sprite_path': None
}

PLAYER_POS = 1.5, 5
PLAYER_ANGLE = 0
PLAYER_SPEED = 0.004
PLAYER_ROT_SPEED = 0.002

# Phone settings 
PHONE_DATA = {
    'size': 30,
    'speed': 200,
    'sprite_path': None
}


# Satiety settings
SATIETY_DATA = {
    'start': 100.0,
    'decrease_rate': 0.067,
    'increase_amount': 10
}

# Raycasting settings
RES = WIDTH, HEIGHT
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
TILE_SIZE = 60

FOV = math.pi / 2
HALF_FOV = FOV / 2

NUM_RAYS = WIDTH // 2
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 20

SCREEN_DIST = HALF_WIDTH / math.tan(HALF_FOV)
SCALE = WIDTH // NUM_RAYS

TEXTURE_SIZE = 256
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2
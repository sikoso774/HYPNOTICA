from os.path import dirname, abspath, join
from os import walk # Utile pour l'import des ressources


# Paramètres globaux du jeu Hypnotica
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
FPS = 60

GAME_TITLE = "Hypnotica"

COLORS = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'gray': (128, 128, 128),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'purple': (127, 0, 255),
    'orange': (212, 92, 6),
}

# --- NOUVELLES CONSTANTES CENTRALES (Chemins de base) ---
# Ces chemins sont relatifs à la racine du projet, qui sera ensuite traitée par 'get_resource_path'
ASSETS_DIR = join("assets")
FONTS_DIR = join(ASSETS_DIR, "fonts")
AUDIO_DIR = join(ASSETS_DIR, "audio")
SOUND_DIR = join(AUDIO_DIR, "sounds")
IMAGES_DIR = join(ASSETS_DIR, "images")

# Police par défaut
DEFAULT_FONT_NAME = join(FONTS_DIR, "MINDCONTROL.ttf")

# Sons des boutons (doivent être traités par audio_importer)
SOUND_CLICK_FILE = 'yes_clicked'  # Nom du fichier sans extension
SOUND_HOVER_FILE = 'hover_click' # Nom du fichier sans extension
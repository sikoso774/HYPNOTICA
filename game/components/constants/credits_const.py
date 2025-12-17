from ...config.settings import *
from ...config.utils import *

# Répertoires et chemins des ressources pour les crédits
TITLE_COLOR = COLORS['green']
TEXT_COLOR = COLORS['white']
IMAGE_PATH = get_resource_path(os.path.join(IMAGES_DIR, "Zoléni_Cyberpunk.jpg"))
# Contenu des crédits
CREDITS_CONTENT = [
    {'type': 'text', 'value': "Credits", 'font_size': 60, 'color': TITLE_COLOR},
    {'type': 'spacer', 'height': 80}, # Espacement
    {'type': 'text', 'value': "Developer : Sikoso 774", 'font_size': 32, 'color': TEXT_COLOR},
    {'type': 'spacer', 'height': 150},
    {'type': 'image', 'value': "developer_image", 'image_path': IMAGE_PATH, 'image_scale_factor': 0.5}, # chemin direct pour l'image
    {'type': 'spacer', 'height': 50},
    {'type': 'text', 'value': "Musics :", 'font_size': 30, 'color': TEXT_COLOR},
    {'type': 'text', 'value': "waera - harinezumi [NCS Release]", 'font_size': 24, 'color': COLORS['gray']},
    {'type': 'text', 'value': "Licensed under Creative Commons", 'font_size': 20, 'color': COLORS['gray']},
    {'type': 'spacer', 'height': 30},
    {'type': 'text', 'value': "Max Brhon - AI [NCS Release]", 'font_size': 24, 'color': COLORS['gray']},
    {'type': 'text', 'value': "Licensed under Creative Commons", 'font_size': 20, 'color': COLORS['gray']},
    {'type': 'spacer', 'height': 30},
    {'type': 'text', 'value': "More Plastic - Rewind [NCS Release]", 'font_size': 24, 'color': COLORS['gray']},
    {'type': 'text', 'value': "Licensed under Creative Commons", 'font_size': 20, 'color': COLORS['gray']},
    {'type': 'spacer', 'height': 50},

    {'type': 'text', 'value': "Game Concept : HYPNOTICA", 'font_size': 28, 'color': COLORS['purple']},
    {'type': 'spacer', 'height': 50},
    {'type': 'text', 'value': "Special Thanks :", 'font_size': 30, 'color': TEXT_COLOR},
    {'type': 'text', 'value': "- My family and friends", 'font_size': 24, 'color': TEXT_COLOR},
    {'type': 'text', 'value': "- Pygame Community", 'font_size': 24, 'color': TEXT_COLOR},
    # {'type': 'text', 'value': "- Google Gemini (for refactoring tips!)", 'font_size': 24, 'color': COLORS['white']},
    {'type': 'spacer', 'height': 80},
    {'type': 'text', 'value': "Thank You For Playing!", 'font_size': 40, 'color': COLORS['green']},
    {'type': 'spacer', 'height': 150}, # Grand espacement pour la fin
    {'type': 'text', 'value': "Press Q to Quit", 'font_size': 24, 'color': COLORS['red']},
    {'type': 'text', 'value': "Press M to Main Menu", 'font_size': 24, 'color': COLORS['blue']},
]
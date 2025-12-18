# Fichier: game/constants/mainmenu_const.py
from ...config.settings import *

# Dimensions des boutons (peuvent rester ici car spécifiques au menu)
BUTTON_WITDH = 250
BUTTON_HEIGHT = 60
BUTTON_SPACING = 20
BUTTON_ACTIVE_COLOR  = COLORS['orange']
BUTTON_INACTIVE_COLOR  = COLORS['gray']

# Calcul dynamique du point de départ vertical (centré ou décalé)
START_Y = HEIGHT // 2 - 50

# Configuration des boutons (Texte, Action, Position Y)
BUTTONS_MENU = [
    {'text': 'JOUER', 
     'action': 'game', 
     'y_offset': START_Y },
    
    {'text': 'INSTRUCTIONS', 
     'action': 'instructions', 
     'y_offset': START_Y + (BUTTON_HEIGHT + BUTTON_SPACING)},
    
    {'text': 'CREDITS', 
     'action': 'credits', 
     'y_offset': START_Y + (BUTTON_HEIGHT + BUTTON_SPACING) * 2},
    
    {'text': 'QUITTER', 
     'action': 'quit', 
     'y_offset': START_Y + (BUTTON_HEIGHT + BUTTON_SPACING) * 3}
]
from game.config import *
from .button_const import *

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
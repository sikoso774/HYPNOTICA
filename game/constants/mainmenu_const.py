from ..config.settings import COLORS, WINDOW_HEIGHT, join

# --- CONFIGURATION DES BOUTONS ---
# Utilisation des constantes de settings.py pour les couleurs
BUTTON_ACTIVE_COLOR = COLORS['orange']
BUTTON_INACTIVE_COLOR = COLORS['gray']

# Liste des boutons (centrés sur la largeur de l'écran)
BUTTON_WITDH = 200
BUTTON_HEIGHT = 45
BUTTON_SPACING = 20


Y_START_BOUTON = WINDOW_HEIGHT // 2 + 50

# Hauteur totale d'un bloc bouton + espacement
BUTTON_BLOCK_HEIGHT = BUTTON_HEIGHT + BUTTON_SPACING 

BUTTONS_MENU = [
    {'text': 'Démarrer', 'action': 'game', 'y_offset': Y_START_BOUTON},
    {'text': 'Crédits', 'action': 'credits', 'y_offset': Y_START_BOUTON + BUTTON_BLOCK_HEIGHT * 1},
    {'text': 'Instructions', 'action': 'instructions', 'y_offset': Y_START_BOUTON + BUTTON_BLOCK_HEIGHT * 2},
    {'text': 'Quitter', 'action': 'quit', 'y_offset': Y_START_BOUTON + BUTTON_BLOCK_HEIGHT * 3},
]
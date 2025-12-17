import pygame
# On importe les constantes globales de la configuration centrale
from ...config.settings import *
from ...config.utils import get_resource_path # On garde get_resource_path

# --- Dimensions de l'écran (maintenant importées de settings.py) ---
LARGEUR_ECRAN_JEU = WINDOW_WIDTH
HAUTEUR_ECRAN_JEU = WINDOW_HEIGHT
TITRE_FENETRE_JEU = "HYPNOTICA"

# --- Couleurs (utilisez directement COLORS['NOM'] de settings.py) ---
# NOTE : Les variables individuelles (NOIR, BLANC) sont redondantes. 
# Si vous tenez à les garder, utilisez: NOIR = COLORS['black']

# --- Police ---
CHEMIN_POLICE_JEU = get_resource_path(DEFAULT_FONT_NAME) # Utilisation de join() pour plus de propreté
TAILLE_POLICE_JEU = 35

# --- Paramètres du Joueur ---
PLAYER_SIZE = 50 
PLAYER_SPEED = 300

# --- Paramètres du Téléphone ---
PHONE_SIZE = 30 
PHONE_SPEED = 120

# --- Paramètres de Satiété ---
SATIETY_START = 100.0
SATIETY_DECREASE_RATE = 0.05
SATIETY_INCREASE_AMOUNT = 10

# --- Chemins des ressources pour le jeu ---
PLAYER_SPRITE_PATH = None 
PHONE_SPRITE_PATH = None 
# Chemin du dossier GIF pour le background (utilise les constantes de settings.py)
GIF_FOLDER_NAME = "hypnose_frames" # Nom du sous-dossier
# Nous laisserons Background ou MainMenu construire le chemin absolu avec get_resource_path
import os
import sys
from os.path import join
from .settings import WINDOW_WIDTH, WINDOW_HEIGHT

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


def folder_importer(*path) -> dict:
    """Importer un dossier et retourner un dictionnaire des chemins absolus vers les fichiers qu'il contient.
    
    Args:
        *paths: Une série de segments de chemin relatifs (ex: "assets", "images").
        
    Returns:
        dict: Un dictionnaire où la clé est le nom du fichier (sans extension) et la valeur est son chemin absolu.
    """
    
    folder_dict = {}

    for folder_path, _, file_names in os.walk(join(*path)):
        for file_name in file_names:
            # On génère la clé (nom sans l'extension)
            key = file_name.split('.')[0]
            # On obtient le chemin absolu pour le fichier en utilisant get_resource_path()
            # On joint le chemin du dossier trouvé par walk (folder_path) et le nom du fichier
            absolute_path = get_resource_path(join(folder_path, file_name))
            
            folder_dict[key] = absolute_path
            
    return folder_dict

def audio_importer(*path) -> dict:
    """Importer des fichiers audio en utilisant le chemin absolu.
    Args:
        *path: Une série de segments de chemin relatifs.
    Returns:
        dict: Un dictionnaire avec les chemins absolus vers les fichiers audio.
    """
    audio_dict = {}
    for folder_path, _, file_names in os.walk(os.path.join(*path)):
        for file_name in file_names:
            key = file_name.split('.')[0]
            absolute_path = get_resource_path(join(folder_path, file_name))
            if file_name.lower().endswith(('.wav', '.ogg')):
                # Sons courts chargés comme des objets Sound
                audio_dict[key] = pygame.mixer.Sound(absolute_path)
            else:
                # Musiques ou autres fichiers audio
                audio_dict[key] = absolute_path
            
    return audio_dict

def image_importer(*path) -> dict:
    """Importer des fichiers images et les charger comme des surfaces Pygame.
    
    Args:
        *paths: Une série de segments de chemin relatifs (ex: "assets", "images").
        
    Returns:
        dict: Un dictionnaire où la clé est le nom de l'image et la valeur est l'objet pygame.Surface chargé.
    """
    
    # 1. Utiliser la fonction modifiée pour obtenir le dictionnaire des chemins absolus
    path_dict = folder_importer(*path)
    image_dict = {}
    
    # 2. Charger chaque image dans Pygame
    for key, path in path_dict.items():
        # Utilisation de pygame.image.load pour charger l'image
        # La méthode .convert_alpha() est recommandée pour les images avec transparence (PNG)
        image_dict[key] = pygame.image.load(path).convert_alpha()
        
    return image_dict

# Test de la fonction folder_impoter
if __name__ == "__main__":
    import pygame
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    folder_path = folder_importer("assets", "images")
    print(f"Chemin absolu vers le dossier 'assets/images': {folder_path}")
    
    # music_files = audio_importer("assets", "audio")
    # print(music_files)
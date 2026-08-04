import pygame as pg
from ..config.settings import *

HYPNOSIS_FOLDER_NAME = "hypnose_frames"

class Animation_GIF:
    def __init__(self, folder_path, screen):
        self.screen = screen
        self.folder_path = folder_path
        self.frames = self.loader_gif_images(folder_path)
        self.frame_counter = 0
        self.animation_frame = 0
        self.animation_speed = 2 # Nombre de ticks avant de changer de frame
                
    def loader_gif_images(self, folder_path):
        """
        Charge toutes les images d'un dossier donné (les frames du GIF).
        """
        frames = []
        
        # walk parcourt les dossiers et fichiers
        for root, _, files in os.walk(self.folder_path):
            sorted_files = sorted(files) 
            
            for file_name in sorted_files:
                if file_name.endswith(('.png', '.jpg', '.jpeg')):
                    try:
                        # Chemin complet de l'image
                        full_path = join(root, file_name)
                        
                        # Charger et convertir l'image (optimisation pour Pygame)
                        img = pg.image.load(full_path).convert() 
                        
                        # Redimensionner l'image à la taille de l'écran si nécessaire
                        img = pg.transform.scale(img, (self.screen.get_width(), self.screen.get_height()))
                        
                        frames.append(img)
                    except pg.error as e:
                        print(f"Erreur de chargement de la frame GIF '{file_name}': {e}")
            
            # Si le dossier est vide, cette liste sera vide, ce qui cause la KeyError
            if not frames:
                print(f"ALERTE : Aucune image trouvée dans le dossier GIF : {folder_path}")
                # Créez une surface noire de secours pour éviter le crash
                placeholder = pg.Surface((self.screen.get_width(), self.screen.get_height()))
                placeholder.fill(COLORS['black'])
                frames.append(placeholder)
                
            return frames
    
    def animate(self):
        """
        Met à jour l'index de la frame à afficher en fonction de la vitesse définie.
        """
        # 1. Incrémenter le compteur de frames du jeu
        self.frame_counter += 1
        
        # 2. Vérifier si le temps est écoulé pour changer de frame GIF
        if self.frame_counter >= self.animation_speed:
            self.frame_counter = 0
            
            # Avoid KeyError by ensuring there are frames to animate
            self.animation_frame += 1
            self.animation_frame %= len(self.frames)
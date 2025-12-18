import pygame as pg
import math
from game.config.settings import *

class RayCaster:
    def __init__(self, game):
        self.game = game
        self.map_obj = game.map  # On récupérera l'objet Map du jeu
        
    def ray_cast(self):
        ox, oy = self.game.player.pos # Position du joueur
        x_map, y_map = int(ox), int(oy)
        
        ray_angle = self.game.player.angle - HALF_FOV + 0.0001
        
        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            # --- Horizontales ---
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a
            
            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor[0] < 0 or tile_hor[0] >= self.map_obj.cols or tile_hor[1] < 0 or tile_hor[1] >= self.map_obj.rows:
                    depth_hor = MAX_DEPTH # Hors map
                    break
                if self.map_obj.grid[tile_hor[1]][tile_hor[0]] == 1: # Mur trouvé
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # --- Verticales ---
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a

            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert[0] < 0 or tile_vert[0] >= self.map_obj.cols or tile_vert[1] < 0 or tile_vert[1] >= self.map_obj.rows:
                    depth_vert = MAX_DEPTH
                    break
                if self.map_obj.grid[tile_vert[1]][tile_vert[0]] == 1: # Mur trouvé
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            # Comparaison et Correction Fisheye
            if depth_vert < depth_hor:
                depth = depth_vert
            else:
                depth = depth_hor
                
            # Correction de l'effet "Fisheye" (distorsion sur les bords)
            depth *= math.cos(self.game.player.angle - ray_angle)

            # Dessin du mur
            # Hauteur perçue = distance_plan / distance_réelle
            proj_height = SCREEN_DIST / (depth + 0.0001) 
            
            # On définit une couleur basée sur la distance (brouillard simple)
            color = [255 / (1 + depth ** 5 * 0.00002)] * 3
            pg.draw.rect(self.game.screen, color, 
                         (ray * SCALE, HEIGHT // 2 - proj_height // 2, SCALE, proj_height))

            ray_angle += DELTA_ANGLE

    def update(self):
        self.ray_cast()
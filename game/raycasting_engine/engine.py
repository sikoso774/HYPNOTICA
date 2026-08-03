import pygame as pg
import math
from game.config.settings import *

class RayCasting:
    def __init__(self, game):
        self.game = game
        
    def ray_cast(self):
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos
        
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

            depth_hor_final = MAX_DEPTH # Valeur par défaut
            wall_id_hor = None

            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    depth_hor_final = depth_hor
                    wall_id_hor = self.game.map.world_map[tile_hor]
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

            depth_vert_final = MAX_DEPTH # Valeur par défaut
            wall_id_vert = None

            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map:
                    depth_vert_final = depth_vert
                    wall_id_vert = self.game.map.world_map[tile_vert]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            # Comparaison : on garde le mur le plus proche, son ID et l'orientation de la face touchée
            # (wall_id sera utilisé pour choisir la texture par type de mur ; is_vertical_hit existe déjà
            # pour ça en raycasting classique, ici en plus pour varier légèrement l'ombrage)
            if depth_vert_final < depth_hor_final:
                depth = depth_vert_final
                wall_id = wall_id_vert
                is_vertical_hit = True
            else:
                depth = depth_hor_final
                wall_id = wall_id_hor
                is_vertical_hit = False

            # Correction Fisheye
            depth *= math.cos(self.game.player.angle - ray_angle)

            # Dessin du mur (Projection 3D)
            proj_height = SCREEN_DIST / (depth + 0.0001)

            # Couleur simple (brouillard) pour tester sans textures
            color_intensity = 255 / (1 + depth ** 5 * 0.00002)
            if is_vertical_hit:
                color_intensity *= 0.85 # Assombrit légèrement les faces verticales (perpendiculaires)
            color = (color_intensity, color_intensity, color_intensity)
            
            # On dessine un rectangle centré verticalement
            pg.draw.rect(self.game.screen, color, 
                         (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height))

            ray_angle += DELTA_ANGLE

    def update(self):
        self.ray_cast()
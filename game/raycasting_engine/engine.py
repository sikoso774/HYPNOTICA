import pygame as pg
import math
from game.config.settings import *

class RayCasting:
    def __init__(self, game):
        self.game = game
        self.wall_textures = self._load_wall_textures()

    def _load_wall_textures(self):
        """
        Textures de mur par wall_id, à bandes verticales. Procédurales en
        attendant de vraies textures d'assets — le motif à bandes permet de
        vérifier visuellement que le mapping offset -> colonne fonctionne.
        """
        palette = {
            1: ((140, 90, 60), (110, 70, 45)),   # terracotta
            2: ((90, 100, 110), (70, 80, 90)),   # pierre grise
        }
        return {wall_id: self._make_striped_texture(*colors) for wall_id, colors in palette.items()}

    def _make_striped_texture(self, base_color, accent_color):
        surf = pg.Surface((TEXTURE_SIZE, TEXTURE_SIZE))
        stripe_width = TEXTURE_SIZE // 8
        for x in range(0, TEXTURE_SIZE, stripe_width):
            color = base_color if (x // stripe_width) % 2 == 0 else accent_color
            pg.draw.rect(surf, color, (x, 0, stripe_width, TEXTURE_SIZE))
        return surf


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

            # Comparaison : on garde le mur le plus proche, son ID, l'orientation de la face touchée
            # et l'offset (position fractionnaire 0-1 du point d'impact sur la face), qui donne la
            # colonne de texture à afficher.
            if depth_vert_final < depth_hor_final:
                depth = depth_vert_final
                wall_id = wall_id_vert
                is_vertical_hit = True
                offset = y_vert % 1
                if cos_a < 0:
                    offset = 1 - offset
            else:
                depth = depth_hor_final
                wall_id = wall_id_hor
                is_vertical_hit = False
                offset = x_hor % 1
                if sin_a < 0:
                    offset = 1 - offset

            # Correction Fisheye
            depth *= math.cos(self.game.player.angle - ray_angle)

            # Dessin du mur (Projection 3D)
            proj_height = SCREEN_DIST / (depth + 0.0001)
            # Bornée : très près d'un mur, proj_height peut exploser bien au-delà de l'écran,
            # ce que pg.transform.scale refuse (au-delà de l'écran, le rendu est identique de toute façon)
            proj_height_int = min(int(proj_height), HEIGHT * 4)

            # Ombrage par distance (+ faces verticales légèrement assombries pour les distinguer)
            brightness = 255 / (1 + depth ** 5 * 0.00002)
            if is_vertical_hit:
                brightness *= 0.85
            brightness = max(0, min(255, brightness))

            texture = self.wall_textures.get(wall_id)
            if texture is not None and proj_height_int > 0:
                tex_x = int(offset * (TEXTURE_SIZE - SCALE))
                wall_column = texture.subsurface(tex_x, 0, SCALE, TEXTURE_SIZE)
                wall_column = pg.transform.scale(wall_column, (SCALE, proj_height_int))
                wall_column.fill((brightness, brightness, brightness), special_flags=pg.BLEND_RGB_MULT)
                self.game.screen.blit(wall_column, (ray * SCALE, HALF_HEIGHT - proj_height_int // 2))
            else:
                # Filet de sécurité si un wall_id n'a pas de texture associée
                color = (brightness, brightness, brightness)
                pg.draw.rect(self.game.screen, color,
                             (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height))

            ray_angle += DELTA_ANGLE

    def update(self):
        self.ray_cast()
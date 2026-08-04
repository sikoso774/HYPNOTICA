import pygame as pg
import math
from game.config.settings import *


class RayCasting:
    """DDA-style raycaster: casts a ray per screen column and draws textured wall slices."""

    def __init__(self, game):
        self.game = game
        self.wall_textures = self._load_wall_textures()

    def _load_wall_textures(self):
        """
        Wall textures per wall_id, with vertical stripes. Procedural while
        waiting for real asset textures — the striped pattern lets us
        visually verify that the offset -> column mapping works correctly.
        """
        palette = {
            1: ((140, 90, 60), (110, 70, 45)),   # terracotta
            2: ((90, 100, 110), (70, 80, 90)),   # gray stone
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

            # --- Horizontal ---
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a

            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            depth_hor_final = MAX_DEPTH # Default value
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

            # --- Vertical ---
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a

            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            depth_vert_final = MAX_DEPTH # Default value
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

            # Comparison: keep the nearest wall, its ID, the orientation of the hit face,
            # and the offset (fractional 0-1 position of the hit point on the face), which
            # gives the texture column to display.
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

            # Fisheye correction
            depth *= math.cos(self.game.player.angle - ray_angle)

            # Wall drawing (3D projection)
            proj_height = SCREEN_DIST / (depth + 0.0001)
            # Clamped: very close to a wall, proj_height can explode well beyond the screen,
            # which pg.transform.scale rejects (beyond the screen, the render looks the same anyway)
            proj_height_int = min(int(proj_height), HEIGHT * 4)

            # Distance shading (+ vertical faces slightly darkened to tell them apart)
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
                # Safety net in case a wall_id has no associated texture
                color = (brightness, brightness, brightness)
                pg.draw.rect(self.game.screen, color,
                             (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height))

            ray_angle += DELTA_ANGLE

    def update(self):
        self.ray_cast()
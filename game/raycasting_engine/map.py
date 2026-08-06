import pygame as pg
from game.config import * # Make sure the import path is correct for your structure

_ = False
# Keeping your mini_map as defined in your file
# (wall_id 1 = terracotta, 2 = gray stone, 3 = glowing exit marker -- see RayCasting._load_wall_textures)
mini_map = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, _, _, 1, _, _, _, _, _, _, 1, _, _, _, _, _, 1],
        [1, _, _, 1, _, _, _, _, _, _, 1, _, _, _, _, _, 1],
        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
        [1, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
        [1, _, _, _, _, _, _, _, _, _, 2, 2, 2, 2, _, _, 1],
        [1, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
        [1, _, 1, _, _, 2, _, _, _, _, _, _, _, _, _, _, 3],
        [1, _, 1, _, _, 2, _, _, _, _, _, _, _, 1, _, _, 3],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Open floor tile facing the glowing exit marker on the right border wall.
EXIT_POS = (15, 7)


class Map:
    """Converts the hardcoded mini_map grid into a world_map dict for O(1) wall lookups."""

    def __init__(self, game):
        self.game = game
        self.mini_map = mini_map
        self.world_map = {}
        self.rows = len(self.mini_map)
        self.cols = len(self.mini_map[0])
        self.get_map()

    def get_map(self):
        # Fill the world_map dictionary with the walls
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i, j)] = value

    def draw(self):
        # Debug function: draws the walls in 2D (top-down view)
        # Uses TILE_SIZE defined in your settings
        [pg.draw.rect(self.game.screen, 'darkgray',
                      (pos[0] * TILE_SIZE, pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE), 2)
         for pos in self.world_map]
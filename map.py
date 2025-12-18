import numpy as np
import pygame as pg
from ..config.settings import *

_ = False
mini_map = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, _, _, 1, _, _, _, _, _, _, 1, _, _, _, 1],
        [1, _, _, 1, _, _, _, _, _, _, 1, _, _, _, 1],
        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
        [1, 1, _, _, _, _, _, _, _, _, _, _, _, _, 1],
        [1, _, _, _, _, _, _, _, _, _, 1, 1, 1, 1, 1],
        [1, _, 1, _, _, _, _, _, _, _, _, _, _, _, 1],
        [1, _, 1, _, _, 1, _, _, _, _, _, _, _, _, 1],
        [1, _, 1, _, _, 1, _, _, _, _, _, _, _, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, _, _, 1],
]
class Map:
    def __init__(self, game):
        self.game = game
        screen = pg.display.get_surface()
        self.mini_map = mini_map
        self.world_map = {}
        self.get_map()
        self.rows = len(mini_map)
        self.cols = len(mini_map)
    
    def get_map(self):
        for j, row, in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i, j)] = value
    
    def draw(self):
        [pg.draw.rect(self.game.screen, 'darkgray', (pos[0] * TILE_SIZE, pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE), 2)
        for pos in self.world_map]


if __name__ == "__main__":
    map = Map()
    print(map.cols, map.rows)
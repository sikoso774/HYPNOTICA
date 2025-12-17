import numpy as np
import pygame as pg

_ = False
class Map:
    
    def __init__(self):
        self.grid = [
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

        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        
    def render(self):
        for i in range(self.rows):
            for j in range(self.cols):
                # pixel coordinates
                tile_x = j * TILESIZE
                tile_y = i * TILESIZE

                if self.grid[i][j] == 0:
                    pg.draw.rect(screen, (255, 255, 255), (tile_x, tile_y, TILESIZE - 1, TILESIZE - 1 ))
                elif self.grid[i][j] == 1:
                    pg.draw.rect(screen, (40, 40, 40), (tile_x, tile_y, TILESIZE - 1, TILESIZE - 1))
                else:
                    pg.draw.rect(screen, (40, 40, 40), (tile_x, tile_y, TILESIZE - 1, TILESIZE - 1))
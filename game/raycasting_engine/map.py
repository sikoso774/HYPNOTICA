import pygame as pg
from game.config import * # Assure-toi que le chemin d'import est bon selon ta structure

_ = False
# On garde ta mini_map définie dans ton fichier
mini_map = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, _, _, 1, _, _, _, _, _, _, 1, _, _, _, _, _, 1],
        [1, _, _, 1, _, _, _, _, _, _, 1, _, _, _, _, _, 1],
        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
        [1, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
        [1, _, _, _, _, _, _, _, _, _, 1, 1, 1, 1, _, _, 1],
        [1, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
        [1, _, 1, _, _, 1, _, _, _, _, _, _, _, _, _, _, 1],
        [1, _, 1, _, _, 1, _, _, _, _, _, _, _, 1, _, _, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

class Map:
    def __init__(self, game):
        self.game = game
        self.mini_map = mini_map
        self.world_map = {}
        self.rows = len(self.mini_map)
        self.cols = len(self.mini_map[0])
        self.get_map()
    
    def get_map(self):
        # On remplit le dictionnaire world_map avec les murs
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i, j)] = value

    def draw(self):
        # Fonction de débogage : dessine les murs en 2D (vue de dessus)
        # On utilise TILE_SIZE défini dans tes settings
        [pg.draw.rect(self.game.screen, 'darkgray', 
                      (pos[0] * TILE_SIZE, pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE), 2)
         for pos in self.world_map]
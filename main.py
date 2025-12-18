import sys
import pygame
from game.game import Game
from map import Map

if __name__ == '__main__':
    pygame.init()
# On crée l'instance du jeu qui gère tout (écrans, sons, boucle)
    game = Game()
    game.run()
import sys
from game.game import Game

if __name__ == '__main__':
# On crée l'instance du jeu qui gère tout (écrans, sons, boucle)
    game = Game() 
    game.run()
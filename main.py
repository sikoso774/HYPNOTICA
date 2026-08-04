import pygame as pg
import sys

# Game config
from game.config import *
from game.core import Intro, MainMenu, Instructions, GameOver, Credits, Level3D, WorldMap


class Game:
    """Owns the display surface, sound manager, and the top-level screen state machine."""

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(GAME_TITLE)
        self.clock = pg.time.Clock()
        self.delta_time = self.clock.tick(FPS) / 1000
        self.current_state = 'start'
        self.setup()

    def setup(self):
        self.sound = Sound(self)
        self.intro = Intro(self)
        self.main_menu = MainMenu(self)
        self.world_map = WorldMap(self)
        self.level = Level3D(self)
        self.game_over = GameOver(self)
        self.instruction = Instructions(self)
        self.credits = Credits(self)

    def update(self):
        action = None
        if self.current_state == 'start':
            action = self.intro.run()
        elif self.current_state == 'menu':
            action = self.main_menu.run()
        elif self.current_state == 'world_map':
            action = self.world_map.run()
        elif self.current_state == 'instructions':
            action = self.instruction.run()
        elif self.current_state == 'credits':
            action = self.credits.run()

        elif self.current_state == 'game':
            # Recreate the level to reset the run (optional)
            self.level = Level3D(self)
            action = self.level.run()

        elif self.current_state == 'game_over':
            action = self.game_over.run()

        # --- Transition handling ---
        if action == 'quit':
            pg.quit()
            sys.exit()

        elif action:
            self.current_state = action # State change (e.g. "menu" -> "game")

    def run(self):
        """Main loop that delegates control to the screens."""
        while True:
            self.update()


if __name__ == "__main__":
    game = Game()
    game.run()
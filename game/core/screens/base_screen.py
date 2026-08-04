# File: game/core/base_screen.py
import pygame as pg
import sys
from game.config import FPS


class BaseScreen:
    """Base class for all screens, implementing the shared check/update/draw loop."""

    def __init__(self, game):
        self.game = game
        self.screen = game.screen  # Direct access to the screen via the Game object
        self.sound = game.sound    # Access to the sound manager
        self.clock = pg.time.Clock()
        self.running = True

    def check_events(self):
        """Base event handler."""
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.quit_game()

            # Hook for child classes (e.g. key press)
            action = self.on_event(event)
            if action:
                return action
        return None

    def on_event(self, event):
        """To be overridden by children to handle screen-specific inputs."""
        return None

    def update(self):
        """Update logic (animations, scroll, etc)."""
        pass

    def draw(self):
        """Draw to the screen."""
        pass

    def quit_game(self):
        pg.quit()
        sys.exit()

    def run(self):
        if hasattr(self, 'music_name') and self.music_name:
            self.sound.play_music(self.music_name)

        self.running = True
        while self.running:
            # 1. Events
            action = self.check_events()
            if action:
                return action

            # 2. Update: modified to capture a return value (e.g. end of intro)
            update_action = self.update()
            if update_action:
                return update_action  # If update returns "menu", we exit!

            # 3. Draw
            self.draw()

            # 4. Update
            pg.display.flip()
            self.clock.tick(FPS)
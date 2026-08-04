import pygame as pg
from game.core.screens import BaseScreen
from game.config.settings import *
from game.raycasting_engine import *


class Level3D(BaseScreen):
    """The raycasting-based gameplay level: wires up the map, player, and raycaster each frame."""

    def __init__(self, game):
        super().__init__(game)
        self.music_name = 'game'
        # Load the font for the Timer (uses the one from settings or the default one)
        try:
            self.font = pg.font.Font(DEFAULT_FONT_NAME, 40)
        except Exception as e:
            print(f"Error loading font: {e}")
            self.font = pg.font.Font(None, 40)
        self.reset()

    def reset(self):
        """Resets the level and the Timer."""

        # --- TIMER CONFIG ---
        self.time_left = 60.0  # Time in seconds (e.g. 60 seconds)

        self.map = Map(self.game)
        self.game.map = self.map

        self.player = Player(self.game)
        self.game.player = self.player

        self.raycaster = RayCasting(self.game)

    def update(self):
        fps = self.clock.get_fps()
        pg.display.set_caption(f'{GAME_TITLE} | FPS : {fps}')
        # Get the time elapsed since the last frame (in milliseconds)
        dt_ms = self.clock.get_time()
        # Store dt in seconds for the player speed calculations
        self.game.dt = dt_ms

        # --- TIMER LOGIC ---
        # Subtract the elapsed time (converted to seconds)
        self.time_left -= dt_ms / 1000.0

        # If time has run out, trigger Game Over
        if self.time_left <= 0:
            self.time_left = 0 # So we don't display a negative number
            return "game_over" # Returns the action to the Game Controller

        # Update the rest of the game
        self.player.update()

        return None

    def draw(self):
        # 1. Background and Raycasting
        self.screen.fill('black')
        pg.draw.rect(self.screen, (30,30,30), (0, HEIGHT//2, WIDTH, HEIGHT//2))
        self.raycaster.update()

        # 2. Debug (optional, comment out for the final render)
        # self.map.draw()
        # self.player.draw()

        # 3. USER INTERFACE (UI) - The Timer
        # Format the text (e.g. "TIME: 45.2")
        timer_text = f"TEMPS: {self.time_left:.1f}"

        # Color change: red if < 10 seconds, otherwise white
        text_color = COLORS['red'] if self.time_left < 10 else COLORS['white']

        # Create the text surface
        text_surface = self.font.render(timer_text, True, text_color)

        # Positioning at the top center
        text_rect = text_surface.get_rect(center=(WIDTH // 2, 50))

        # Display
        self.screen.blit(text_surface, text_rect)
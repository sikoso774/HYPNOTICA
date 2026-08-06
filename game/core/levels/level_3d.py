import math
import pygame as pg
from game.core.screens import BaseScreen
from game.config.settings import *
from game.raycasting_engine import *
from game.raycasting_engine.map import EXIT_POS

# --- Invisible presence (tension mechanic) ---
DANGER_START_DISTANCE = 14.0   # buffer, in "tiles", before it catches the player
DANGER_BASE_RATE = 0.5         # tiles/sec it closes in, even while the player moves
DANGER_STILL_MULTIPLIER = 3.0  # extra creep rate while the player stands still
TICK_INTERVAL_FAR_MS = 1800    # time between audio "tics" when the presence is far
TICK_INTERVAL_NEAR_MS = 220    # time between tics right before it catches the player
VIGNETTE_MAX_ALPHA = 180


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

        # --- PRESENCE STATE ---
        self.danger_distance = DANGER_START_DISTANCE
        self._last_player_pos = self.player.pos
        self._last_tick_time = pg.time.get_ticks()

    def update(self):
        fps = self.clock.get_fps()
        pg.display.set_caption(f'{GAME_TITLE} | FPS : {fps}')
        # Get the time elapsed since the last frame (in milliseconds)
        dt_ms = self.clock.get_time()
        # Store dt in seconds for the player speed calculations
        self.game.dt = dt_ms
        dt_s = dt_ms / 1000.0

        # --- TIMER LOGIC ---
        # Subtract the elapsed time (converted to seconds)
        self.time_left -= dt_s

        # If time has run out, trigger Game Over
        if self.time_left <= 0:
            self.time_left = 0 # So we don't display a negative number
            self.game.game_over_reason = 'timeout'
            return "game_over" # Returns the action to the Game Controller

        # Update the rest of the game
        self.player.update()

        # --- WIN CHECK ---
        if self.player.map_pos == EXIT_POS:
            return "level_complete"

        # --- PRESENCE LOGIC ---
        px, py = self.player.pos
        last_px, last_py = self._last_player_pos
        moved = abs(px - last_px) + abs(py - last_py)
        self._last_player_pos = (px, py)

        creep_rate = DANGER_BASE_RATE * (DANGER_STILL_MULTIPLIER if moved < 1e-6 else 1.0)
        self.danger_distance -= creep_rate * dt_s

        if self.danger_distance <= 0:
            self.game.game_over_reason = 'caught'
            return "game_over"

        # Audio "tic" that speeds up as the presence gets closer
        proximity = 1.0 - max(0.0, min(1.0, self.danger_distance / DANGER_START_DISTANCE))
        tick_interval = TICK_INTERVAL_FAR_MS - (TICK_INTERVAL_FAR_MS - TICK_INTERVAL_NEAR_MS) * proximity
        now = pg.time.get_ticks()
        if now - self._last_tick_time > tick_interval:
            self.sound.play_sfx('click')
            self._last_tick_time = now

        return None

    def draw(self):
        # 1. Background and Raycasting
        self.screen.fill('black')
        pg.draw.rect(self.screen, (30,30,30), (0, HEIGHT//2, WIDTH, HEIGHT//2))
        self.raycaster.update()

        # 2. Debug (optional, comment out for the final render)
        # self.map.draw()
        # self.player.draw()

        # 3. Presence vignette: barely visible while it's far, ramps up fast as it closes in
        self._draw_danger_vignette()

        # 4. USER INTERFACE (UI) - The Timer
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

    def _draw_danger_vignette(self):
        proximity = 1.0 - max(0.0, min(1.0, self.danger_distance / DANGER_START_DISTANCE))
        alpha = int(VIGNETTE_MAX_ALPHA * proximity ** 2)
        if alpha <= 0:
            return
        overlay = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        pulse = 0.85 + 0.15 * math.sin(pg.time.get_ticks() * 0.01)
        pg.draw.rect(overlay, (120, 0, 0, int(alpha * pulse)), overlay.get_rect(), width=60)
        self.screen.blit(overlay, (0, 0))

import pygame as pg
import math
from ..config.settings import *


class Player:
    """Tracks the player's position/angle in map coordinates and handles movement input."""

    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0

        # Using self.game.dt to make movement framerate-independent
        speed = PLAYER_SPEED * self.game.dt
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()
        if keys[pg.K_z] or keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx -= speed_cos
            dy -= speed_sin
        if keys[pg.K_q] or keys[pg.K_a]:
            dx += speed_sin
            dy -= speed_cos
        if keys[pg.K_d]:
            dx -= speed_sin
            dy += speed_cos

        if keys[pg.K_LEFT]:
            self.angle -= PLAYER_ROT_SPEED * self.game.dt
        if keys[pg.K_RIGHT]:
            self.angle += PLAYER_ROT_SPEED * self.game.dt

        self.check_wall_collision(dx, dy)
        self.angle %= math.tau

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        # Simple sliding collision
        if self.check_wall(int(self.x + dx * 3), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * 3)):
            self.y += dy

    def update(self):
        self.movement()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    def draw(self):
        # 2D debug
        pg.draw.line(self.game.screen, 'yellow', (self.x * TILE_SIZE, self.y * TILE_SIZE),
                    (self.x * TILE_SIZE + WIDTH * math.cos(self.angle),
                     self.y * TILE_SIZE + WIDTH * math.sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'green', (self.x * TILE_SIZE, self.y * TILE_SIZE), 15)
from __future__ import annotations
import math
import random
import pygame
from entities.base_entity import BaseEntity
from constants import *

class Asteroid(BaseEntity):
    def __init__(self, world_x: float, world_y: float, speed_mult: float = 1.0) -> None:
        super().__init__(world_x, world_y)
        self._radius: int = random.randint(ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS)
        
        # Kustas uz leju pretī spēlētājam
        angle = random.uniform(math.pi * 0.2, math.pi * 0.8) 
        speed = random.uniform(80, 150) * speed_mult
        self._vx: float = math.cos(angle) * speed
        self._vy: float = math.sin(angle) * speed

        self._shape_points = self._gen_shape()
        self._craters = self._gen_craters()
        self._angle: float = random.uniform(0, 360)
        self._rot_speed: float = random.uniform(-40, 40)

    def _gen_shape(self) -> list:
        pts = []
        for i in range(random.randint(8, 12)):
            base_a = 2 * math.pi * i / 10
            r = self._radius * random.uniform(0.75, 1.0)
            pts.append((math.cos(base_a) * r, math.sin(base_a) * r))
        return pts

    def _gen_craters(self) -> list:
        craters = []
        for _ in range(random.randint(1, 3)):
            r_c = random.randint(3, max(4, self._radius // 4))
            dist = random.uniform(0, self._radius * 0.5)
            angle = random.uniform(0, 2 * math.pi)
            craters.append((math.cos(angle) * dist, math.sin(angle) * dist, r_c))
        return craters

    @property
    def radius(self) -> int: return self._radius
    @property
    def damage_amount(self) -> int:
        if self._radius < 20: return ASTEROID_DMG_SMALL
        elif self._radius < 35: return ASTEROID_DMG_MEDIUM
        return ASTEROID_DMG_LARGE

    def update(self, dt: float) -> None:
        self._x += self._vx * dt
        self._y += self._vy * dt
        self._angle += self._rot_speed * dt

        # Atlec no ekrāna sāniem (X ass)
        if self._x < self._radius:
            self._x = self._radius
            self._vx *= -1
        elif self._x > SCREEN_WIDTH - self._radius:
            self._x = SCREEN_WIDTH - self._radius
            self._vx *= -1

    def draw(self, surface: pygame.Surface, cam_offset_y: float) -> None:
        sx, sy = int(self._x), int(self.screen_y(cam_offset_y))
        if not self.is_on_screen(cam_offset_y): return

        rad = math.radians(self._angle)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        rotated = [(sx + cos_a * px - sin_a * py, sy + sin_a * px + cos_a * py) for px, py in self._shape_points]

        pygame.draw.polygon(surface, C_ASTEROID, rotated)
        pygame.draw.polygon(surface, C_ASTER_LIGHT, rotated, 2)

        for cx, cy, cr in self._craters:
            pygame.draw.circle(surface, C_ASTER_DARK, (sx + int(cos_a * cx - sin_a * cy), sy + int(sin_a * cx + cos_a * cy)), cr)

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(int(self._x) - self._radius, int(self._y) - self._radius, self._radius * 2, self._radius * 2)

    def get_screen_rect(self, cam_offset_y: float) -> pygame.Rect:
        sy = self.screen_y(cam_offset_y)
        return pygame.Rect(int(self._x) - self._radius, int(sy) - self._radius, self._radius * 2, self._radius * 2)
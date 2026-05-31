"""
Kuģa klase / Ship class
"""
from __future__ import annotations
import math
import pygame

from entities.base_entity import BaseEntity
from constants import *

class Ship(BaseEntity):
    def __init__(self) -> None:
        # Kuģa Y ir atkarīgs no kameras, sākotnēji to piešķir gameplay.py
        super().__init__(float(SHIP_SCREEN_X), 0.0)

        self._health: float = float(SHIP_MAX_HEALTH)
        self._fuel:   float = float(SHIP_MAX_FUEL)

        self._bounce_vx:    float = 0.0
        self._bounce_vy:    float = 0.0
        self._bounce_time:  float = 0.0 

        self._anim_time: float = 0.0
        self._fuel_save_timer: float = 0.0
        self._emergency_used: bool = False

    @property
    def health(self) -> float: return self._health
    @health.setter
    def health(self, value: float) -> None: self._health = max(0.0, min(float(value), float(SHIP_MAX_HEALTH)))
    @property
    def fuel(self) -> float: return self._fuel
    @fuel.setter
    def fuel(self, value: float) -> None: self._fuel = max(0.0, min(float(value), float(SHIP_MAX_FUEL)))

    @property
    def is_out_of_fuel(self) -> bool: return self._fuel <= 0.0
    @property
    def is_out_of_health(self) -> bool: return self._health <= 0.0
    @property
    def emergency_used(self) -> bool: return self._emergency_used
    @emergency_used.setter
    def emergency_used(self, value: bool) -> None: self._emergency_used = value
    @property
    def screen_x(self) -> float: return self._x

    def take_damage(self, amount: float) -> None: self.health -= amount
    def heal(self, amount: float) -> None: self.health += amount
    def add_fuel(self, amount: float) -> None: self.fuel += amount
    def start_fuel_saving(self) -> None: self._fuel_save_timer = BREAKDOWN_FUEL_SAVE_TIME

    def bounce_away(self, dir_x: float, dir_y: float) -> None:
        self._bounce_vx   = dir_x * SHIP_BOUNCE_SPEED
        self._bounce_time = SHIP_BOUNCE_TIME

    def update(self, dt: float) -> None:
        self._anim_time += dt

        if self._fuel_save_timer > 0:
            self._fuel_save_timer -= dt
        elif not self.is_out_of_fuel:
            self.fuel -= SHIP_FUEL_DRAIN * dt

        if self._bounce_time > 0:
            self._bounce_time -= dt
            factor = self._bounce_time / SHIP_BOUNCE_TIME
            self._x += self._bounce_vx * factor * dt
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]: self._x -= SHIP_SPEED_X * dt
            if keys[pygame.K_RIGHT]: self._x += SHIP_SPEED_X * dt
            
        # Ierobežo ekrānā
        self._x = max(SHIP_WIDTH // 2, min(SCREEN_WIDTH - SHIP_WIDTH // 2, self._x))

    def draw(self, surface: pygame.Surface, cam_offset_y: float = 0) -> None:
        """Zīmē kuģi statiski uz ekrāna (SHIP_SCREEN_Y)"""
        cx = int(self._x)
        cy = int(SHIP_SCREEN_Y) 
        w, h  = SHIP_WIDTH, SHIP_HEIGHT

        self._draw_flames(surface, cx, cy, w, h)
        self._draw_body(surface, cx, cy, w, h)
        self._draw_cockpit(surface, cx, cy, w, h)
        self._draw_engine_glow(surface, cx, cy, w, h)

    def _draw_flames(self, s, cx, cy, w, h) -> None:
        pulse = 0.7 + 0.3 * math.sin(self._anim_time * 12)
        self._draw_single_flame(s, cx - w // 5, cy + h // 2 - 2, pulse)
        self._draw_single_flame(s, cx + w // 5, cy + h // 2 - 2, pulse)
        self._draw_single_flame(s, cx, cy + h // 2, pulse, scale=1.3)

    def _draw_single_flame(self, s, fx, fy, pulse, scale=1.0) -> None:
        fh, fw = int((14 + 6 * pulse) * scale), int((8  + 2 * pulse) * scale)
        pygame.draw.polygon(s, C_FLAME_OUT, [(fx, fy), (fx - fw, fy + fh), (fx + fw, fy + fh)])
        pygame.draw.polygon(s, C_FLAME_MID, [(fx, fy + 2), (fx - fw//2, fy + fh), (fx + fw//2, fy + fh)])
        pygame.draw.polygon(s, C_FLAME_CORE, [(fx, fy + 4), (fx - fw//4, fy + int(fh*0.7)), (fx + fw//4, fy + int(fh*0.7))])

    def _draw_body(self, s, cx, cy, w, h) -> None:
        hw, hh = w // 2, h // 2
        wing_top, wing_bot = cy - hh // 2, cy + hh // 3
        left_wing  = [(cx - hw//2, wing_top), (cx - hw, wing_bot + 10), (cx - hw//3, wing_bot)]
        right_wing = [(cx + hw//2, wing_top), (cx + hw, wing_bot + 10), (cx + hw//3, wing_bot)]
        pygame.draw.polygon(s, C_SHIP_WING, left_wing)
        pygame.draw.polygon(s, C_SHIP_WING, right_wing)
        pygame.draw.polygon(s, C_SHIP_ACCENT, left_wing,  2)
        pygame.draw.polygon(s, C_SHIP_ACCENT, right_wing, 2)

        body_pts = [(cx - hw // 3, cy - hh), (cx + hw // 3, cy - hh), (cx + hw // 2 - 2, cy + hh - 4), (cx - hw // 2 + 2, cy + hh - 4)]
        pygame.draw.polygon(s, C_SHIP_BODY, body_pts)
        pygame.draw.polygon(s, C_SHIP_ACCENT, body_pts, 2)

    def _draw_cockpit(self, s, cx, cy, w, h) -> None:
        cab_w, cab_h = w // 3 + 2, h // 4 + 4
        cab_rect = pygame.Rect(cx - cab_w//2, cy - (h // 2) - cab_h//2 + 4, cab_w, cab_h)
        pygame.draw.ellipse(s, C_COCKPIT_D, cab_rect)
        pygame.draw.ellipse(s, C_COCKPIT_L, pygame.Rect(cab_rect.x + 3, cab_rect.y + 2, cab_w - 10, cab_h - 6))

    def _draw_engine_glow(self, s, cx, cy, w, h) -> None:
        pulse = 0.8 + 0.2 * math.sin(self._anim_time * 8)
        glow_color = (int(C_ENGINE[0] * pulse), int(C_ENGINE[1] * pulse), int(C_ENGINE[2] * pulse))
        pygame.draw.rect(s, glow_color, pygame.Rect(cx - 6, cy + h // 2 - 6, 12, 10), border_radius=3)

    def get_rect(self) -> pygame.Rect:
        """Atgriež ekrāna koordinātas, jo kuģis stāv uz vietas ekrānā."""
        return pygame.Rect(int(self._x) - SHIP_WIDTH // 2, int(SHIP_SCREEN_Y) - SHIP_HEIGHT // 2, SHIP_WIDTH, SHIP_HEIGHT)
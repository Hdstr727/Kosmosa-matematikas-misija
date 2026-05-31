"""
Kosmosa fons / Space background renderer

Trīs slāņu parallax efekts:
  - Tālas zvaigznes (lēni skrull)
  - Tuvas zvaigznes (ātrāk)
  - Spoža nebuloza (statiska)
"""

from __future__ import annotations
import random
import math
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class StarLayer:
    """
    Viens zvaigžņu slānis ar parallax kustību.

    === Iekapsulesana ===
    Zvaigžņu pozīcijas glabātas privāti — ārējs kods tikai izsauc draw().
    """

    def __init__(self, count: int, speed_factor: float,
                 min_size: int, max_size: int,
                 color_range: tuple[int, int]) -> None:
        self._speed:  float = speed_factor
        self._stars:  list  = []

        lo, hi = color_range
        for _ in range(count):
            x    = random.randint(0, SCREEN_WIDTH)
            y    = random.randint(0, SCREEN_HEIGHT)
            size = random.randint(min_size, max_size)
            bright = random.randint(lo, hi)
            self._stars.append([x, y, size, (bright, bright, bright + 10)])

    def draw(self, surface: pygame.Surface, cam_offset_y: float) -> None:
        """Zīmē slāni ņemot vērā kameras nobīdi (parallax)."""
        for x, base_y, size, color in self._stars:
            # Parallax: tālāks slānis kustās lēnāk
            y = int((base_y - cam_offset_y * self._speed) % SCREEN_HEIGHT)
            if size == 1:
                surface.set_at((int(x), y), color)
            else:
                pygame.draw.circle(surface, color, (int(x), y), size)


class Background:
    """
    Pilns kosmosa fons ar vairākiem slāņiem.

    === Iekapsulesana ===
    Visi slāņi un nebuloza glabāti privāti.
    Publiskā metode: draw(surface, cam_offset_y)
    """

    def __init__(self) -> None:
        # Trīs zvaigžņu slāņi ar dažādu parallax ātrumu
        self._layer_far  = StarLayer(180, 0.05, 1, 1, (60,  110))
        self._layer_mid  = StarLayer(100, 0.15, 1, 2, (100, 170))
        self._layer_near = StarLayer(40,  0.30, 2, 3, (160, 220))

        # Priekšģenerētas nebulozu plankumi
        self._nebulae = self._gen_nebulae()

    def _gen_nebulae(self) -> list:
        """Ģenerē nejaušas nebulozu plankuma pozīcijas un izmērus."""
        result = []
        colors = [
            (20, 10, 60, 30),    # violets
            (0,  20, 50, 25),    # tumši zils
            (30, 5,  40, 20),    # purpurs
        ]
        for _ in range(6):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            rx = random.randint(60, 180)
            ry = random.randint(40, 120)
            color = random.choice(colors)
            result.append((x, y, rx, ry, color))
        return result

    def draw(self, surface: pygame.Surface, cam_offset_y: float) -> None:
        """Zīmē visu fonu: nebulozas + trīs zvaigžņu slāņi."""
        # 1. Pamata fona krāsa
        surface.fill((4, 4, 18))

        # 2. Nebulozu plankumi (alfa-blending)
        for x, base_y, rx, ry, color in self._nebulae:
            y = int((base_y - cam_offset_y * 0.03) % SCREEN_HEIGHT)
            r, g, b, a = color
            neb_surf = pygame.Surface((rx * 2, ry * 2), pygame.SRCALPHA)
            # Gradient efekts — vairāki apļi ar mazāku alpha
            for scale in [1.0, 0.7, 0.45]:
                aa = int(a * scale * 0.6)
                w  = int(rx * 2 * scale)
                h  = int(ry * 2 * scale)
                tmp = pygame.Surface((w, h), pygame.SRCALPHA)
                pygame.draw.ellipse(tmp, (r, g, b, aa), (0, 0, w, h))
                neb_surf.blit(tmp, (rx - w // 2, ry - h // 2))
            surface.blit(neb_surf, (x - rx, y - ry))

        # 3. Zvaigžņu slāņi (tāls → tuvs)
        self._layer_far.draw(surface, cam_offset_y)
        self._layer_mid.draw(surface, cam_offset_y)
        self._layer_near.draw(surface, cam_offset_y)

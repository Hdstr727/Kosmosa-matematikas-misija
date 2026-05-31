"""
Partikulu sistēma / Particle system

=== OOP Koncepti ===
- Iekapsulesana: katra partikula ir atsevišķs objekts ar privātiem atribūtiem
- ParticleSystem pārvalda visu partikulu dzīves ciklu
"""

from __future__ import annotations
import random
import math
import pygame


class Particle:
    """
    Viena partikula — vizuāls efekts sadursmei vai savākšanai.
    """
    def __init__(self, x: float, y: float, color: tuple,
                 vx: float, vy: float, lifetime: int, size: int = 4) -> None:
        self._x:        float = x
        self._y:        float = y
        self._color:    tuple = color
        self._vx:       float = vx
        self._vy:       float = vy
        self._lifetime: int   = lifetime    
        self._age:      int   = 0           
        self._size:     int   = size

    @property
    def alive(self) -> bool:
        return self._age < self._lifetime

    def update(self) -> None:
        """Pārvieto partikulu un palielina vecumu."""
        self._x  += self._vx
        self._y  += self._vy
        self._vy += 0.12   # Gravitācija
        self._vx *= 0.97   # Berze
        self._age += 1

    def draw(self, surface: pygame.Surface) -> None:
        """Zīmē partikulu ar izbalēšanas efektu."""
        if not self.alive:
            return
        progress = 1.0 - self._age / self._lifetime   # 1.0 → 0.0
        alpha = int(255 * progress)
        size  = max(1, int(self._size * progress))

        # Krāsa ar alpha
        r, g, b = self._color[:3]
        surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (r, g, b, alpha), (size, size), size)
        surface.blit(surf, (int(self._x) - size, int(self._y) - size))


class ParticleSystem:
    """
    Pārvalda visas aktīvās partikulas.
    """
    def __init__(self) -> None:
        self._particles: list[Particle] = []

    def spawn_hit(self, x: float, y: float, color: tuple, count: int) -> None:
        """Izveido sadursmes efektu (partikulas izšaujas visās virzienās)."""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1.5, 5.0)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            life = random.randint(25, 55)
            size = random.randint(3, 7)
            self._particles.append(Particle(x, y, color, vx, vy, life, size))

    def spawn_pickup(self, x: float, y: float, color: tuple, count: int) -> None:
        """Izveido savākšanas efektu (partikulas paceļas uz augšu)."""
        for _ in range(count):
            angle = random.uniform(-math.pi, 0)   
            speed = random.uniform(1.0, 4.0)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed - 1.0
            life = random.randint(20, 45)
            size = random.randint(2, 6)
            self._particles.append(Particle(x, y, color, vx, vy, life, size))

    def spawn_trail(self, x: float, y: float, color: tuple) -> None:
        """Dzinēja astes efekts (saucas katru kadru). Maksimālisms!"""
        vx = random.uniform(-0.5, 0.5)
        vy = random.uniform(2.0, 4.0) # Krīt uz leju
        life = random.randint(10, 20)
        size = random.randint(2, 4)
        # Nedaudz randomizē izejas pozīciju (x), lai izskatītos pēc liesmas
        self._particles.append(Particle(x + random.uniform(-10, 10), y, color, vx, vy, life, size))

    def update(self) -> None:
        """Atjaunina visas partikulas un noņem mirušās."""
        for p in self._particles:
            p.update()
        self._particles = [p for p in self._particles if p.alive]

    def draw(self, surface: pygame.Surface) -> None:
        """Zīmē visas partikulas."""
        for p in self._particles:
            p.draw(surface)

    def clear(self) -> None:
        """Notīra visas partikulas (piemēram, līmeņa beigās)."""
        self._particles.clear()
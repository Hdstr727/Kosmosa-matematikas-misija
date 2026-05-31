"""
Uzlabojumu klases / Pickup classes

=== OOP Koncepti ===
- Abstraktā klase: Pickup ir abstrakts (nevar tieši izveidot)
- Mantošana: HealthPickup un FuelPickup manto Pickup, kas manto BaseEntity
  BaseEntity → Pickup → HealthPickup
                      → FuelPickup
- Polimorfisms: apply(), get_particle_color(), get_label() — katrā citādas
- Virtuālās funkcijas: apply() un get_particle_color() ir @abstractmethod
"""

from __future__ import annotations
import math
import pygame
from abc import abstractmethod

from entities.base_entity import BaseEntity
from constants import (
    SCREEN_HEIGHT, SCREEN_WIDTH,
    PICKUP_RADIUS, PICKUP_FLOAT_AMPLITUDE, PICKUP_FLOAT_SPEED,
    HEALTH_PICKUP_VALUE, FUEL_PICKUP_VALUE,
    C_HEALTH_PICK, C_FUEL_PICK, C_WHITE, C_BLACK,
)


# ======================================================================= #
#  Abstraktā bāzklase uzlabojumiem
# ======================================================================= #

class Pickup(BaseEntity):
    """
    Abstraktā bāzklase visiem uzlabojumiem.
    Manto BaseEntity, bet ir pati arī abstrakta.

    Apakšklases (HealthPickup, FuelPickup) OBLIGĀTI ievieš:
      - apply(ship)           — piemēro efektu
      - get_particle_color()  — partikulu krāsa efektam
      - get_label()           — uzraksts (diagnostikai)
    """

    def __init__(self, world_x: float, world_y: float) -> None:
        super().__init__(world_x, world_y)

        # === Iekapsulesana ===
        self._value:      float = 0.0   # Cik lielu bonusu dod (aizstāj apakšklase)
        self._anim_timer: float = 0.0   # Peldēšanas animācija
        self._collected:  bool  = False  # Vai jau savākts

    # ------------------------------------------------------------------ #
    #  Virtuālās funkcijas (apakšklases PĀRRAKSTA)
    # ------------------------------------------------------------------ #

    @abstractmethod
    def apply(self, ship) -> None:
        """
        [VIRTUĀLĀ FUNKCIJA] Piemēro uzlabojuma efektu kuģim.
        Polimorfisms: HealthPickup dziedē, FuelPickup tanko.
        """
        ...

    @abstractmethod
    def get_particle_color(self) -> tuple:
        """[VIRTUĀLĀ FUNKCIJA] Atgriež partikulu krāsu savākšanas brīdī."""
        ...

    @abstractmethod
    def get_label(self) -> str:
        """[VIRTUĀLĀ FUNKCIJA] Atgriež uzlabojuma veida nosaukumu."""
        ...

    # ------------------------------------------------------------------ #
    #  Kopīgas metodes (manto abas apakšklases)
    # ------------------------------------------------------------------ #

    def collect(self, ship) -> None:
        """Savāc uzlabojumu (izsauc apply + atzīmē kā savāktu)."""
        if not self._collected:
            self.apply(ship)
            self._collected = True
            self.destroy()

    @property
    def collected(self) -> bool:
        return self._collected

    # ------------------------------------------------------------------ #
    #  Virtuālā funkcija: update() — peldēšanas animācija
    # ------------------------------------------------------------------ #

    def update(self, dt: float) -> None:
        """
        [Pārraksta BaseEntity.update()]
        Pievieno vertikālu peldēšanas animāciju.
        Abas apakšklases izmanto šo pašu update (nevis pārraksta).
        """
        self._anim_timer += dt

    def _get_visual_y(self, cam_offset_y: float) -> float:
        """Aprēķina vizuālo Y ar peldēšanas efektu."""
        base_sy = self.screen_y(cam_offset_y)
        offset   = math.sin(self._anim_timer * PICKUP_FLOAT_SPEED) * PICKUP_FLOAT_AMPLITUDE
        return base_sy + offset

    # ------------------------------------------------------------------ #
    #  Virtuālā funkcija: get_rect()
    # ------------------------------------------------------------------ #

    def get_rect(self) -> pygame.Rect:
        """[Pārraksta BaseEntity.get_rect()] — pasaules koordinātas."""
        return pygame.Rect(
            int(self._x) - PICKUP_RADIUS,
            int(self._y) - PICKUP_RADIUS,
            PICKUP_RADIUS * 2, PICKUP_RADIUS * 2,
        )

    def get_screen_rect(self, cam_offset_y: float) -> pygame.Rect:
        """Sadursmes taisnstūris ekrāna koordinātās."""
        sy = self._get_visual_y(cam_offset_y)
        return pygame.Rect(
            int(self._x) - PICKUP_RADIUS, int(sy) - PICKUP_RADIUS,
            PICKUP_RADIUS * 2, PICKUP_RADIUS * 2,
        )


# ======================================================================= #
#  Veselības uzlabojums / Health Pickup
# ======================================================================= #

class HealthPickup(Pickup):
    """
    Zaļš krustveida uzlabojums — atjauno kuģa veselību.

    === Mantošana ===
    BaseEntity → Pickup → HealthPickup

    === Polimorfisms ===
    Pārraksta apply() un get_particle_color() savādāk nekā FuelPickup.
    """

    def __init__(self, world_x: float, world_y: float) -> None:
        super().__init__(world_x, world_y)
        self._value = float(HEALTH_PICKUP_VALUE)

    # ------------------------------------------------------------------ #
    #  Virtuālo funkciju ieviešana
    # ------------------------------------------------------------------ #

    def apply(self, ship) -> None:
        """[Pārraksta Pickup.apply()] Dziedē kuģi."""
        ship.heal(self._value)

    def get_particle_color(self) -> tuple:
        """[Pārraksta Pickup.get_particle_color()] Zaļš efekts."""
        return C_HEALTH_PICK

    def get_label(self) -> str:
        return f"+{int(self._value)} veselība"

    def draw(self, surface: pygame.Surface, cam_offset_y: float) -> None:
        """
        [Pārraksta BaseEntity.draw()]
        Zīmē zaļu medicīnas krustu (+).
        """
        if not self.is_on_screen(cam_offset_y, 60):
            return

        cx  = int(self._x)
        cy  = int(self._get_visual_y(cam_offset_y))
        r   = PICKUP_RADIUS

        # Mirdzuma aplis
        glow_surf = pygame.Surface((r * 4, r * 4), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*C_HEALTH_PICK, 45), (r * 2, r * 2), r * 2)
        surface.blit(glow_surf, (cx - r * 2, cy - r * 2))

        # Krustveida forma
        thick = max(6, r // 2)
        # Horizontālā josla
        pygame.draw.rect(surface, C_HEALTH_PICK,
                         (cx - r, cy - thick // 2, r * 2, thick), border_radius=3)
        # Vertikālā josla
        pygame.draw.rect(surface, C_HEALTH_PICK,
                         (cx - thick // 2, cy - r, thick, r * 2), border_radius=3)
        # Baltā apmale (1 pikselis)
        pygame.draw.rect(surface, C_WHITE,
                         (cx - r, cy - thick // 2, r * 2, thick), 1, border_radius=3)
        pygame.draw.rect(surface, C_WHITE,
                         (cx - thick // 2, cy - r, thick, r * 2), 1, border_radius=3)


# ======================================================================= #
#  Degvielas uzlabojums / Fuel Pickup
# ======================================================================= #

class FuelPickup(Pickup):
    """
    Sarkana kanistra ikona — papildina degvielu.

    === Mantošana ===
    BaseEntity → Pickup → FuelPickup

    === Polimorfisms ===
    Pārraksta apply() un get_particle_color() — atšķirīga uzvedība.
    """

    def __init__(self, world_x: float, world_y: float) -> None:
        super().__init__(world_x, world_y)
        self._value = float(FUEL_PICKUP_VALUE)

    # ------------------------------------------------------------------ #
    #  Virtuālo funkciju ieviešana
    # ------------------------------------------------------------------ #

    def apply(self, ship) -> None:
        """[Pārraksta Pickup.apply()] Pievieno degvielu kuģim."""
        ship.add_fuel(self._value)

    def get_particle_color(self) -> tuple:
        """[Pārraksta Pickup.get_particle_color()] Oranžs efekts."""
        return C_FUEL_PICK

    def get_label(self) -> str:
        return f"+{int(self._value)} degviela"

    def draw(self, surface: pygame.Surface, cam_offset_y: float) -> None:
        """
        [Pārraksta BaseEntity.draw()]
        Zīmē sarkanu degvielas kanistru.
        """
        if not self.is_on_screen(cam_offset_y, 60):
            return

        cx  = int(self._x)
        cy  = int(self._get_visual_y(cam_offset_y))
        r   = PICKUP_RADIUS

        # Mirdzuma aplis
        glow_surf = pygame.Surface((r * 4, r * 4), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*C_FUEL_PICK, 45), (r * 2, r * 2), r * 2)
        surface.blit(glow_surf, (cx - r * 2, cy - r * 2))

        # Kanistra korpuss
        body_rect = pygame.Rect(cx - r + 3, cy - r + 4, (r - 3) * 2, r * 2 - 4)
        pygame.draw.rect(surface, C_FUEL_PICK, body_rect, border_radius=4)

        # Kaklina (augšdaļa)
        neck_rect = pygame.Rect(cx - r // 3, cy - r - 2, r // 1.5, 7)
        pygame.draw.rect(surface, C_FUEL_PICK, neck_rect, border_radius=2)

        # Rokturis (loks pa labi)
        handle_rect = pygame.Rect(cx + r - 5, cy - r // 2, 8, r)
        pygame.draw.arc(surface, C_FUEL_PICK,
                        pygame.Rect(cx + r // 2, cy - r // 2, 12, r),
                        math.pi * 0.2, math.pi * 1.8, 4)

        # Baltā svītra kanistrā
        pygame.draw.line(surface, (255, 200, 150),
                         (cx - r + 7, cy - 2), (cx + r - 7, cy - 2), 2)

        # Apmale
        pygame.draw.rect(surface, C_WHITE, body_rect, 1, border_radius=4)

import math  # noqa: E402  (nepieciešams FuelPickup.draw)

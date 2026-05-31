"""
Bāzes entitātes abstraktā klase / Base entity abstract class

=== OOP Koncepti / OOP Concepts ===
- Abstraktā klase (ABC): BaseEntity nevar tieši instancēt
- Virtuālās funkcijas (@abstractmethod): update(), draw(), get_rect()
  — katra apakšklase OBLIGĀTI pārraksta šīs metodes
- Iekapsulesana: stāvoklis glabāts _privātos atribūtos
- Datu slēpsana: piekļuve caur property dekoratoriem
"""

from __future__ import annotations
from abc import ABC, abstractmethod

import pygame

from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class BaseEntity(ABC):
    """
    Abstraktā bāzes klase visiem spēles objektiem.

    Mantošanas hierarhija (kas manto šo klasi):
      BaseEntity
        ├── Ship          (kuģis)
        ├── Asteroid      (asteroīds)
        └── Pickup        (uzlabojumi — arī abstrakts)
              ├── HealthPickup
              └── FuelPickup

    Virtuālās funkcijas, ko apakšklases PĀRRAKSTA:
      - update(dt)         — atjaunina stāvokli
      - draw(screen, ...)  — zīmē objektu
      - get_rect()         — atgriež sadursmes taisnstūri
    """

    def __init__(self, x: float, y: float) -> None:
        """
        Pamata inicializācija ar pozīciju.
        x, y: pasaules koordinātas (world-space)
        """
        # === Iekapsulesana + Datu slēpsana ===
        # Viena "_" prefikss = "aizsargāts" (protected), pieejams apakšklasēm
        self._x: float = x   # Pasaules X koordināta
        self._y: float = y   # Pasaules Y koordināta
        self._alive: bool = True  # Vai objekts ir aktīvs

    # ------------------------------------------------------------------ #
    #  Virtuālās funkcijas (Virtual / Abstract methods)
    # ------------------------------------------------------------------ #

    @abstractmethod
    def update(self, dt: float) -> None:
        """
        [VIRTUĀLĀ FUNKCIJA] Atjaunina objekta stāvokli.
        dt: delta laiks sekundēs kopš pēdējā kadra.
        Katra apakšklase ievieš savu loģiku.
        """
        ...

    @abstractmethod
    def draw(self, surface: pygame.Surface, cam_offset_y: float) -> None:
        """
        [VIRTUĀLĀ FUNKCIJA] Zīmē objektu uz ekrāna.
        surface: pygame Surface (ekrāns)
        cam_offset_y: kameras nobīde pa Y asi (scrolling)
        Katra apakšklase zīmē sevi savādāk — POLIMORFISMS.
        """
        ...

    @abstractmethod
    def get_rect(self) -> pygame.Rect:
        """
        [VIRTUĀLĀ FUNKCIJA] Atgriež sadursmes taisnstūri pasaules coords.
        Izmanto sadursmes noteikšanai (collision detection).
        """
        ...

    # ------------------------------------------------------------------ #
    #  Property dekoratori (Datu slēpsana / Data hiding)
    # ------------------------------------------------------------------ #

    @property
    def x(self) -> float:
        """Publiska lasīšanas piekļuve X koordinātai."""
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        """Kontrolēta X koordinātas iestatīšana."""
        self._x = float(value)

    @property
    def y(self) -> float:
        """Publiska lasīšanas piekļuve Y koordinātai."""
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        """Kontrolēta Y koordinātas iestatīšana."""
        self._y = float(value)

    @property
    def alive(self) -> bool:
        """Vai objekts joprojām ir aktīvs spēlē."""
        return self._alive

    def destroy(self) -> None:
        """Atzīmē objektu kā nedzīvu — to izņems no spēles."""
        self._alive = False

    # ------------------------------------------------------------------ #
    #  Ekrāna koordinātu aprēķins (palīgmetode apakšklasēm)
    # ------------------------------------------------------------------ #

    def screen_y(self, cam_offset_y: float) -> float:
        """
        Pārvērš pasaules Y koordinātu ekrāna Y koordinātā.

        Kameras sistēma:
          screen_y = world_y - cam_offset_y

        cam_offset_y = kuģis._world_y - SHIP_SCREEN_Y
        Tā kuģis vienmēr parādās SHIP_SCREEN_Y pozīcijā.
        """
        return self._y - cam_offset_y

    def is_on_screen(self, cam_offset_y: float, margin: int = 100) -> bool:
        """
        Pārbauda, vai objekts atrodas ekrānā (ar marginu).
        Izmanto, lai nerendētu neredzamos objektus.
        """
        sy = self.screen_y(cam_offset_y)
        return -margin < sy < SCREEN_HEIGHT + margin

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(x={self._x:.1f}, y={self._y:.1f})"

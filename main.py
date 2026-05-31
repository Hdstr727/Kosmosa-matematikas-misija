"""
Kosmosa Matemātikas Misija — Galvenais fails / Main entry point

=== Programmas struktūra ===
main.py
├── constants.py          — visas konstantes
├── game_state.py         — progresa saglabāšana (JSON)
├── level_config.py       — 10 līmeņu parametri
├── background.py         — kosmosa fons (parallax)
├── particles.py          — partikulu sistēma
├── math_tasks.py         — matemātikas uzdevumu ģenerators
├── ui.py                 — pogas, HUD, popup logi, izvēlnes
├── gameplay.py           — spēles sesijas loģika
└── entities/
    ├── base_entity.py    — abstraktā bāzklase (ABC)
    ├── ship.py           — kuģis
    ├── asteroid.py       — asteroīds
    └── pickup.py         — uzlabojumi (Pickup, HealthPickup, FuelPickup)

=== Spēles stāvokļi (State Machine) ===
MAIN_MENU → LEVEL_SELECT → GAMEPLAY → RESULT → (atpakaļ)

=== OOP Koncepti ===
- Iekapsulesana:    katrs modulis/klase slēpj savu stāvokli
- Datu slēpsana:    privāti atribūti ar property
- Mantošana:        Ship, Asteroid, Pickup → BaseEntity
- Polimorfisms:     draw(), update(), get_rect() katrā klasē citādāk
- Virtuālās f-jas: @abstractmethod BaseEntity
"""

import sys
import pygame

from constants      import *
from game_state     import GameState
from level_config   import get_level_config, TOTAL_LEVELS
from background     import Background
from ui             import MainMenu, LevelSelectMenu, ResultScreen, draw_text
from gameplay       import GameSession


# ======================================================================= #
#  Spēles stāvokļu konstantes / Game state constants
# ======================================================================= #

STATE_MAIN_MENU    = "main_menu"
STATE_LEVEL_SELECT = "level_select"
STATE_GAMEPLAY     = "gameplay"
STATE_RESULT       = "result"


# ======================================================================= #
#  Galvenā spēles klase / Main game class
# ======================================================================= #

class Game:
    """
    Galvenā spēles vadības klase.

    Pārvalda:
      - pygame inicializāciju un loga izveidi
      - Stāvokļu mašīnu (state machine)
      - Pārejas starp ekrāniem

    === Iekapsulesana ===
    Pašreizējais stāvoklis, ekrāns, pulkstenis — privāti atribūti.
    Ārējs kods izsauc tikai run().
    """

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption(WINDOW_TITLE)

        self._screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self._clock  = pygame.time.Clock()

        # Saglabātais progress (JSON)
        self._save   = GameState()

        # Stāvokļu mašīna
        self._state:         str        = STATE_MAIN_MENU
        self._selected_level: int | None = None
        self._result_data:   dict | None = None

        # Fons (zīmē zem visiem ekrāniem)
        self._bg = Background()
        self._bg_cam = 0.0   # Lēna fona animācija izvēlnē

        # Ekrānu objekti
        self._main_menu:    MainMenu | None         = None
        self._level_select: LevelSelectMenu | None  = None
        self._result_screen: ResultScreen | None    = None

        self._init_main_menu()

    # ------------------------------------------------------------------ #
    #  Inicializācijas metodes
    # ------------------------------------------------------------------ #

    def _init_main_menu(self) -> None:
        self._state      = STATE_MAIN_MENU
        self._main_menu  = MainMenu()

    def _init_level_select(self) -> None:
        self._state        = STATE_LEVEL_SELECT
        self._level_select = LevelSelectMenu(
            self._save.unlocked_levels,
            self._save.completed_levels,
            TOTAL_LEVELS,
        )

    def _init_gameplay(self, level: int) -> None:
        """Palaiž spēles sesiju un gaida rezultātu."""
        self._state          = STATE_GAMEPLAY
        self._selected_level = level
        cfg                  = get_level_config(level)

        session = GameSession(self._screen, self._clock, cfg)
        result  = session.run()   # Bloķējoša izsaukšana — atgriežas tikai pēc beigām

        # Saglabā progresu ja uzvarēja
        if result["result"] == "win":
            self._save.complete_level(level)

        self._init_result(result["result"], result.get("reason", ""), level)

    def _init_result(self, result: str, reason: str, level: int) -> None:
        self._state         = STATE_RESULT
        self._result_data   = {"result": result, "reason": reason, "level": level}
        self._result_screen = ResultScreen(
            won       = result == "win",
            level_num = level,
            max_level = TOTAL_LEVELS,
        )

    # ------------------------------------------------------------------ #
    #  Galvenais cikls
    # ------------------------------------------------------------------ #

    def run(self) -> None:
        """Palaiž galveno spēles ciklu."""
        while True:
            dt = self._clock.tick(FPS) / 1000.0
            dt = min(dt, 0.05)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self._handle_state(events, dt)

    # ------------------------------------------------------------------ #
    #  Stāvokļu apstrāde
    # ------------------------------------------------------------------ #

    def _handle_state(self, events: list, dt: float) -> None:
        """Apstrādā pašreizējo stāvokli."""
        if self._state == STATE_MAIN_MENU:
            self._run_main_menu(events, dt)
        elif self._state == STATE_LEVEL_SELECT:
            self._run_level_select(events, dt)
        elif self._state == STATE_RESULT:
            self._run_result(events, dt)
        # STATE_GAMEPLAY tiek palaists _init_gameplay() iekšienē (bloķējoša izsaukšana)

    # ------------------------------------------------------------------ #
    #  Galvenās izvēlnes ekrāns
    # ------------------------------------------------------------------ #

    def _run_main_menu(self, events: list, dt: float) -> None:
        self._bg_cam -= 20 * dt   # Lēna fona kustība
        self._bg.draw(self._screen, self._bg_cam)

        for event in events:
            action = self._main_menu.handle_event(event)
            if action == "play":
                self._init_level_select()
                return
            elif action == "exit":
                pygame.quit()
                sys.exit()

        self._main_menu.draw(self._screen, dt)
        pygame.display.flip()

    # ------------------------------------------------------------------ #
    #  Līmeņu izvēles ekrāns
    # ------------------------------------------------------------------ #

    def _run_level_select(self, events: list, dt: float) -> None:
        self._bg_cam -= 15 * dt
        self._bg.draw(self._screen, self._bg_cam)

        for event in events:
            action = self._level_select.handle_event(event)
            if action == "start":
                lvl = self._level_select.selected_level
                if lvl is not None:
                    self._init_gameplay(lvl)   # Ienāk spēlē (bloķē)
                    return
            elif action == "back":
                self._init_main_menu()
                return

        self._level_select.draw(self._screen)
        pygame.display.flip()

    # ------------------------------------------------------------------ #
    #  Rezultātu ekrāns
    # ------------------------------------------------------------------ #

    def _run_result(self, events: list, dt: float) -> None:
        self._bg_cam -= 12 * dt
        self._bg.draw(self._screen, self._bg_cam)

        d = self._result_data
        for event in events:
            action = self._result_screen.handle_event(event)
            if action == "next":
                next_lvl = d["level"] + 1
                self._init_gameplay(next_lvl)
                return
            elif action == "retry":
                self._init_gameplay(d["level"])
                return
            elif action == "menu":
                self._init_main_menu()
                return

        self._result_screen.draw(self._screen, d.get("reason", ""))
        pygame.display.flip()


# ======================================================================= #
#  Ieejas punkts / Entry point
# ======================================================================= #

if __name__ == "__main__":
    game = Game()
    game.run()

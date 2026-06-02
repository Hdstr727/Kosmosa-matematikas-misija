"""
Kosmosa Matemātikas Misija - Galvenais fails / Main entry point
"""
import sys
import pygame

from constants      import *
from game_state     import GameState
from level_config   import get_level_config, TOTAL_LEVELS
from background     import Background
from ui             import MainMenu, LevelSelectMenu, ResultScreen, draw_text
from gameplay       import GameSession

STATE_MAIN_MENU    = "main_menu"
STATE_LEVEL_SELECT = "level_select"
STATE_GAMEPLAY     = "gameplay"
STATE_RESULT       = "result"

class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption(WINDOW_TITLE)

        self.is_fullscreen = False
        self.window_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen = pygame.display.set_mode(self.window_size, pygame.RESIZABLE)
        self.logical_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self._clock  = pygame.time.Clock()
        self._save   = GameState()

        self._state:         str        = STATE_MAIN_MENU
        self._selected_level: int | None = None
        self._result_data:   dict | None = None

        self._bg = Background()
        self._bg_cam = 0.0   

        self._main_menu:    MainMenu | None         = None
        self._level_select: LevelSelectMenu | None  = None
        self._result_screen: ResultScreen | None    = None

        self._init_main_menu()

    def handle_video_event(self, event) -> bool:
        if event.type == pygame.VIDEORESIZE and not self.is_fullscreen:
            self.window_size = (event.w, event.h)
            self.screen = pygame.display.set_mode(self.window_size, pygame.RESIZABLE)
            return True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            self.is_fullscreen = not self.is_fullscreen
            if self.is_fullscreen:
                self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            else:
                self.screen = pygame.display.set_mode(self.window_size, pygame.RESIZABLE)
            return True
        return False

    def map_mouse_pos(self, pos: tuple[int, int]) -> tuple[int, int]:
        """Pārveido peles koordinātas no reālā ekrāna uz loģisko."""
        sw, sh = self.screen.get_size()
        scale_x = SCREEN_WIDTH / sw
        scale_y = SCREEN_HEIGHT / sh
        return (int(pos[0] * scale_x), int(pos[1] * scale_y))

    def _init_main_menu(self) -> None:
        self._state      = STATE_MAIN_MENU
        self._main_menu  = MainMenu()

    def _init_level_select(self) -> None:
        self._state        = STATE_LEVEL_SELECT
        self._level_select = LevelSelectMenu(self._save.unlocked_levels, self._save.completed_levels, TOTAL_LEVELS)

    def _init_gameplay(self, level: int) -> None:
        self._state          = STATE_GAMEPLAY
        self._selected_level = level
        
        session = GameSession(self, get_level_config(level))
        result  = session.run()   

        # Ja spēlētājs iziet no pauzes izvēlnes atpakaļ uz galveno
        if result["result"] == "quit":
            return self._init_main_menu()

        if result["result"] == "win":
            self._save.complete_level(level)

        self._init_result(result["result"], result.get("reason", ""), level)

    def _init_result(self, result: str, reason: str, level: int) -> None:
        self._state         = STATE_RESULT
        self._result_data   = {"result": result, "reason": reason, "level": level}
        self._result_screen = ResultScreen(won=result == "win", level_num=level, max_level=TOTAL_LEVELS)

    def run(self) -> None:
        while True:
            dt = min(self._clock.tick(FPS) / 1000.0, 0.05)
            events = pygame.event.get()
            
            # Peles koordinātu pārveidošana visiem eventi
            for event in events:
                if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                    event.pos = self.map_mouse_pos(event.pos)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if self._state == STATE_MAIN_MENU:
                self._run_main_menu(events, dt)
            elif self._state == STATE_LEVEL_SELECT:
                self._run_level_select(events, dt)
            elif self._state == STATE_RESULT:
                self._run_result(events, dt)

    def _render_and_scale(self, shake_x=0, shake_y=0):
        scaled = pygame.transform.smoothscale(self.logical_surface, self.screen.get_size())
        self.screen.fill(C_BLACK)
        self.screen.blit(scaled, (shake_x, shake_y))
        pygame.display.flip()

    def _run_main_menu(self, events: list, dt: float) -> None:
        self._bg_cam -= 20 * dt   
        self._bg.draw(self.logical_surface, self._bg_cam)

        for event in events:
            if self.handle_video_event(event): continue
            action = self._main_menu.handle_event(event)
            if action == "play": return self._init_level_select()
            elif action == "exit": pygame.quit(); sys.exit()

        self._main_menu.draw(self.logical_surface, dt)
        self._render_and_scale()

    def _run_level_select(self, events: list, dt: float) -> None:
        self._bg_cam -= 15 * dt
        self._bg.draw(self.logical_surface, self._bg_cam)

        for event in events:
            if self.handle_video_event(event): continue
            action = self._level_select.handle_event(event)
            if action == "start" and self._level_select.selected_level is not None:
                return self._init_gameplay(self._level_select.selected_level)
            elif action == "back":
                return self._init_main_menu()

        self._level_select.draw(self.logical_surface)
        self._render_and_scale()

    def _run_result(self, events: list, dt: float) -> None:
        self._bg_cam -= 12 * dt
        self._bg.draw(self.logical_surface, self._bg_cam)

        d = self._result_data
        for event in events:
            if self.handle_video_event(event): continue
            action = self._result_screen.handle_event(event)
            if action == "next": return self._init_gameplay(d["level"] + 1)
            elif action == "retry": return self._init_gameplay(d["level"])
            elif action == "menu": return self._init_main_menu()

        self._result_screen.draw(self.logical_surface, d.get("reason", ""))
        self._render_and_scale()

if __name__ == "__main__":
    Game().run()
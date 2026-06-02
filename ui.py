"""
UI komponentes / UI components

=== OOP Koncepti ===
- Iekapsulesana: katrs UI elements pārvalda savu stāvokli
- Mantošana: Button ir bāzklase visām pogām
- Polimorfisms: draw() katrā pogā var atšķirties
"""

from __future__ import annotations
import math
import pygame

from constants import *


# ======================================================================= #
#  Fontu kešs (vienreiz inicializē, izmanto visur)
# ======================================================================= #

_font_cache: dict[int, pygame.font.Font] = {}


def get_font(size: int) -> pygame.font.Font:
    """Atgriež kešotu fontu norādītā izmērā."""
    if size not in _font_cache:
        try:
            # Izmantojam Arial, jo tas ir uz visām OS un atbalsta latviešu burtus
            _font_cache[size] = pygame.font.SysFont("arial", size, bold=True)
        except Exception:
            _font_cache[size] = pygame.font.Font(None, size)
    return _font_cache[size]


def draw_text(surface: pygame.Surface, text: str, size: int,
              color: tuple, x: int, y: int,
              anchor: str = "center") -> pygame.Rect:
    """
    Palīgfunkcija teksta zīmēšanai ar norādītu enkuru.
    anchor: "center", "topleft", "topright", "midleft"
    """
    font = get_font(size)
    img  = font.render(text, True, color)
    rect = img.get_rect()
    setattr(rect, anchor, (x, y))
    surface.blit(img, rect)
    return rect


# ======================================================================= #
#  Poga / Button
# ======================================================================= #

class Button:
    """
    Klikšķināma poga ar hover efektu.
    """
    def __init__(self, x: int, y: int, w: int, h: int,
                 text: str, font_size: int = FS_MED) -> None:
        self._rect:      pygame.Rect = pygame.Rect(x - w // 2, y - h // 2, w, h)
        self._text:      str         = text
        self._font_size: int         = font_size
        self._hovered:   bool        = False

    @property
    def rect(self) -> pygame.Rect:
        return self._rect

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            self._hovered = self._rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._rect.collidepoint(event.pos):
                return True
        return False

    def draw(self, surface: pygame.Surface) -> None:
        color = C_BTN_HOV if self._hovered else C_BTN
        pygame.draw.rect(surface, color, self._rect, border_radius=10)
        pygame.draw.rect(surface, C_BTN_TXT, self._rect, 2, border_radius=10)
        draw_text(surface, self._text, self._font_size, C_BTN_TXT,
                  self._rect.centerx, self._rect.centery)


# ======================================================================= #
#  HUD - galvas augšējais displejs
# ======================================================================= #

class HUD:
    """
    Spēles HUD: veselības josla, degvielas josla, kļūdu skaitītājs,
    ārkārtas degvielas poga, progresa josla.
    """
    BAR_W  = 220
    BAR_H  = 22
    BAR_Y  = SCREEN_HEIGHT - 52
    HLTH_X = 30
    FUEL_X = SCREEN_WIDTH - 30 - 220

    def draw(self, surface: pygame.Surface,
             health: float, max_health: float,
             fuel: float, max_fuel: float,
             strikes: int, max_strikes: int,
             emergency_available: bool,
             progress_ratio: float = 0.0) -> None:
        
        self._draw_bar(surface, self.HLTH_X, self.BAR_Y, health, max_health, C_HEALTH, C_HEALTH_DIM, TXT_HEALTH)
        self._draw_bar(surface, self.FUEL_X, self.BAR_Y, fuel, max_fuel, C_FUEL, C_FUEL_DIM, TXT_FUEL)
        self._draw_strikes(surface, strikes, max_strikes)
        self._draw_emergency(surface, emergency_available)
        self._draw_progress_bar(surface, progress_ratio)

    def _draw_progress_bar(self, surface, ratio):
        start_y = SCREEN_HEIGHT - 120
        end_y = 60
        x = SCREEN_WIDTH - 20
        
        pygame.draw.line(surface, C_PROG_BG, (x, start_y), (x, end_y), 4)
        pygame.draw.line(surface, C_FINISH_LINE, (x - 10, end_y), (x + 10, end_y), 4)
        
        current_y = start_y - (start_y - end_y) * ratio
        pygame.draw.circle(surface, C_PROG_FG, (int(x), int(current_y)), 6)
        pygame.draw.circle(surface, C_WHITE, (int(x), int(current_y)), 2)

    def _draw_bar(self, surface, x, y, val, max_val, color, dim, label) -> None:
        bg_rect = pygame.Rect(x, y, self.BAR_W, self.BAR_H)
        pygame.draw.rect(surface, C_HUD_BG, bg_rect, border_radius=5)
        pygame.draw.rect(surface, dim, bg_rect, border_radius=5)
        fill_w = int(self.BAR_W * max(0, val) / max_val)
        if fill_w > 0:
            pygame.draw.rect(surface, color, pygame.Rect(x, y, fill_w, self.BAR_H), border_radius=5)
        pygame.draw.rect(surface, C_WHITE, bg_rect, 1, border_radius=5)
        draw_text(surface, label, FS_SMALL, color, x, y - 18, anchor="topleft")
        draw_text(surface, f"{int(val)}/{int(max_val)}", FS_SMALL, C_WHITE, x + self.BAR_W, y - 18, anchor="topright")

    def _draw_strikes(self, surface, strikes, max_strikes) -> None:
        draw_text(surface, TXT_STRIKES, FS_SMALL, C_WHITE, SCREEN_WIDTH // 2, 14, anchor="center")
        r, spacing, start_x = 12, 34, SCREEN_WIDTH // 2 - (max_strikes - 1) * 34 // 2
        for i in range(max_strikes):
            cx, cy = start_x + i * spacing, 42
            color = C_STRIKE_ON if i < strikes else C_STRIKE_OFF
            d = 7
            pygame.draw.line(surface, color, (cx - d, cy - d), (cx + d, cy + d), 3)
            pygame.draw.line(surface, color, (cx + d, cy - d), (cx - d, cy + d), 3)
            pygame.draw.circle(surface, color, (cx, cy), r, 2)

    def _draw_emergency(self, surface, available: bool) -> None:
        x, y = SCREEN_WIDTH - 30 - 54, SCREEN_HEIGHT - 52 - 60
        color = C_EMERGENCY if available else C_EMERG_USED
        rect = pygame.Rect(x, y, 54, 54)
        pygame.draw.rect(surface, C_HUD_BG, rect, border_radius=8)
        pygame.draw.rect(surface, color, rect, 2, border_radius=8)
        icon_x, icon_y = x + 27, y + 20
        pygame.draw.rect(surface, color, pygame.Rect(icon_x - 10, icon_y - 8, 20, 18), border_radius=3)
        pygame.draw.rect(surface, color, (icon_x - 5, icon_y - 13, 10, 6), border_radius=2)
        for i, line in enumerate(TXT_EMERG_FUEL.split("\n")):
            draw_text(surface, line, 11, color, x + 27, y + 58 + i * 12, anchor="center")


# ======================================================================= #
#  Matemātikas / Avārijas uznirstošais logs
# ======================================================================= #

class TaskPopup:
    POP_W = 620
    POP_H = 280
    POP_X = (SCREEN_WIDTH  - POP_W) // 2
    POP_Y = (SCREEN_HEIGHT - POP_H) // 2

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self._input = ""
        self._result = ""
        self._correct_ans = ""
        self._result_t = 0.0

    @property
    def input_text(self) -> str:
        return self._input

    def handle_key(self, event: pygame.event.Event) -> str:
        if event.type != pygame.KEYDOWN:
            return ""
        if event.key == pygame.K_BACKSPACE:
            self._input = self._input[:-1]
        elif event.key == pygame.K_RETURN:
            return "submit"
        elif event.unicode in "0123456789,.-":
            if len(self._input) < 12:
                self._input += event.unicode
        return ""

    def show_result(self, kind: str, correct_ans: str = "") -> None:
        self._result = kind
        self._correct_ans = correct_ans
        self._result_t = 2.0  

    def update(self, dt: float) -> bool:
        if self._result and self._result_t > 0:
            self._result_t -= dt
            if self._result_t <= 0:
                return True
        return False

    def draw(self, surface: pygame.Surface, question: str,
             time_left: float, max_time: float,
             is_breakdown: bool = False) -> None:
        bg_color  = C_BREAK_BG  if is_breakdown else C_POPUP_BG
        bdr_color = C_BREAK_BDR if is_breakdown else C_POPUP_BDR
        title_txt = TXT_BREAKDOWN if is_breakdown else TXT_MATH_TASK

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        surface.blit(overlay, (0, 0))

        rect = pygame.Rect(self.POP_X, self.POP_Y, self.POP_W, self.POP_H)
        pygame.draw.rect(surface, bg_color, rect, border_radius=16)
        pygame.draw.rect(surface, bdr_color, rect, 3, border_radius=16)

        draw_text(surface, title_txt, FS_MED, bdr_color, SCREEN_WIDTH // 2, self.POP_Y + 26, anchor="center")
        draw_text(surface, question, FS_LARGE, C_WHITE, SCREEN_WIDTH // 2, self.POP_Y + 80, anchor="center")

        inp_rect = pygame.Rect(self.POP_X + 80, self.POP_Y + 120, self.POP_W - 160, 46)
        inp_color = C_INPUT_ACTI if not self._result else (40, 40, 60)
        pygame.draw.rect(surface, inp_color, inp_rect, border_radius=8)
        pygame.draw.rect(surface, bdr_color, inp_rect, 2, border_radius=8)

        display_txt = self._input + ("|" if not self._result else "")
        draw_text(surface, TXT_ANSWER, FS_SMALL, C_BTN_TXT, inp_rect.x, inp_rect.y - 22, anchor="topleft")
        draw_text(surface, display_txt, FS_LARGE, C_WHITE, inp_rect.centerx, inp_rect.centery, anchor="center")

        if not self._result:
            self._draw_timer(surface, time_left, max_time, bdr_color)
        else:
            self._draw_result(surface)

        if not self._result:
            draw_text(surface, TXT_CONFIRM, FS_SMALL, (100, 120, 180), SCREEN_WIDTH // 2, self.POP_Y + self.POP_H - 20, anchor="center")

    def _draw_timer(self, surface, time_left, max_time, color) -> None:
        tw, tx, ty = self.POP_W - 160, self.POP_X + 80, self.POP_Y + 188
        pygame.draw.rect(surface, (30, 30, 55), (tx, ty, tw, 12), border_radius=6)
        ratio = max(0, time_left / max_time)
        bar_color = C_TIMER_LOW if ratio < 0.3 else C_TIMER_BAR
        fill_w = int(tw * ratio)
        if fill_w > 0:
            pygame.draw.rect(surface, bar_color, (tx, ty, fill_w, 12), border_radius=6)
        draw_text(surface, f"{time_left:.1f}s", FS_SMALL, bar_color, tx + tw // 2, ty - 20, anchor="center")

    def _draw_result(self, surface) -> None:
        if self._result == "correct": txt, color = TXT_CORRECT, C_CORRECT
        elif self._result == "wrong": txt, color = TXT_WRONG_ANS, C_WRONG
        else: txt, color = TXT_TIMEOUT, C_WRONG
        
        y_off = self.POP_Y + 185
        draw_text(surface, txt, FS_LARGE, color, SCREEN_WIDTH // 2, y_off, anchor="center")

        if self._result in ("wrong", "timeout") and self._correct_ans:
            draw_text(surface, f"Pareizā atbilde: {self._correct_ans}", FS_MED, C_GOLD, SCREEN_WIDTH // 2, y_off + 35, anchor="center")


# ======================================================================= #
#  Finiša līnija
# ======================================================================= #

def draw_finish_line(surface: pygame.Surface, cam_offset_y: float,
                     world_height: float, scroll_speed: float) -> None:
    screen_y = -cam_offset_y
    if -60 < screen_y < SCREEN_HEIGHT + 60:
        sy = int(screen_y)
        pygame.draw.rect(surface, C_FINISH_LINE, (0, sy - 4, SCREEN_WIDTH, 8))
        draw_text(surface, TXT_FINISH, FS_LARGE, C_FINISH_LINE, SCREEN_WIDTH // 2, sy - 30, anchor="center")


# ======================================================================= #
#  Pauzes Izvēlne / Pause Menu
# ======================================================================= #

class PauseMenu:
    def __init__(self) -> None:
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        self._buttons = {
            "resume": Button(cx, cy - 30, 240, 58, TXT_RESUME, FS_LARGE),
            "quit":   Button(cx, cy + 50, 240, 58, TXT_MENU, FS_LARGE),
        }

    def handle_event(self, event: pygame.event.Event) -> str:
        for key, btn in self._buttons.items():
            if btn.handle_event(event): return key
        return ""

    def draw(self, surface: pygame.Surface) -> None:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        draw_text(surface, TXT_PAUSED, FS_HUGE, C_GOLD, cx, cy - 130, anchor="center")

        for btn in self._buttons.values():
            btn.draw(surface)


# ======================================================================= #
#  Uzvaras / Zaudējuma ekrāns
# ======================================================================= #

class ResultScreen:
    def __init__(self, won: bool, level_num: int, max_level: int) -> None:
        self._won      = won
        self._level    = level_num
        self._buttons: dict[str, Button] = {}

        cx, y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60

        if won:
            if level_num < max_level: 
                self._buttons["retry"] = Button(cx - 220, y, 160, 52, TXT_REPLAY)
                self._buttons["next"]  = Button(cx,       y, 220, 52, TXT_NEXT_LVL)
                self._buttons["menu"]  = Button(cx + 220, y, 160, 52, TXT_MENU)
            else:
                self._buttons["retry"] = Button(cx - 120, y, 160, 52, TXT_REPLAY)
                self._buttons["menu"]  = Button(cx + 120, y, 160, 52, TXT_MENU)
        else:
            self._buttons["retry"] = Button(cx - 120, y, 200, 52, TXT_RETRY)
            self._buttons["menu"]  = Button(cx + 120, y, 180, 52, TXT_MENU)

    def handle_event(self, event: pygame.event.Event) -> str:
        for key, btn in self._buttons.items():
            if btn.handle_event(event): return key
        return ""

    def draw(self, surface: pygame.Surface, reason: str = "") -> None:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        surface.blit(overlay, (0, 0))

        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        title = TXT_WIN_TITLE if self._won else TXT_LOSE_TITLE
        color = C_GOLD if self._won else C_WRONG
        draw_text(surface, title, FS_HUGE, color, cx, cy - 90, anchor="center")

        if not self._won and reason:
            draw_text(surface, reason, FS_MED, C_WHITE, cx, cy - 20, anchor="center")

        for btn in self._buttons.values():
            btn.draw(surface)


# ======================================================================= #
#  Galvenā izvēlne / Main menu
# ======================================================================= #

class MainMenu:
    def __init__(self) -> None:
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        self._buttons = {
            "play": Button(cx, cy + 20, 240, 58, TXT_PLAY, FS_LARGE),
            "exit": Button(cx, cy + 100, 240, 58, TXT_EXIT, FS_LARGE),
        }
        self._anim = 0.0

    def handle_event(self, event: pygame.event.Event) -> str:
        for key, btn in self._buttons.items():
            if btn.handle_event(event): return key
        return ""

    def draw(self, surface: pygame.Surface, dt: float) -> None:
        self._anim += dt
        pulse = 0.85 + 0.15 * math.sin(self._anim * 2.0)
        r, g, b = int(100 * pulse), int(205 * pulse), int(255 * pulse)
        
        draw_text(surface, TXT_TITLE, FS_TITLE, (r, g, b), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, anchor="center")
        draw_text(surface, "Kosmosa piedzīvojums", FS_MED, (60, 100, 160), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 58, anchor="center")

        for btn in self._buttons.values(): btn.draw(surface)


# ======================================================================= #
#  Līmeņu izvēlne / Level select menu
# ======================================================================= #

class LevelSelectMenu:
    COLS = 5
    ROWS = 2
    BTN_W = 120
    BTN_H = 100
    GAP_X = 30
    GAP_Y = 30

    def __init__(self, unlocked: set[int], completed: set[int], total: int) -> None:
        self._unlocked  = unlocked
        self._completed = completed
        self._total     = total
        self._selected: int | None = None
        self._hovered:  int | None = None

        grid_w = self.COLS * self.BTN_W + (self.COLS - 1) * self.GAP_X
        grid_h = self.ROWS * self.BTN_H + (self.ROWS - 1) * self.GAP_Y
        self._ox = (SCREEN_WIDTH  - grid_w) // 2
        self._oy = (SCREEN_HEIGHT - grid_h) // 2 + 10

        self._start_btn = Button(SCREEN_WIDTH // 2, self._oy + grid_h + 55, 240, 55, TXT_START, FS_LARGE)
        self._back_btn  = Button(70, 36, 120, 40, TXT_BACK, FS_SMALL)

    @property
    def selected_level(self) -> int | None:
        return self._selected

    def _get_cell_rect(self, level: int) -> pygame.Rect:
        idx  = level - 1
        col  = idx % self.COLS
        row  = idx // self.COLS
        x    = self._ox + col * (self.BTN_W + self.GAP_X)
        y    = self._oy + row * (self.BTN_H + self.GAP_Y)
        return pygame.Rect(x, y, self.BTN_W, self.BTN_H)

    def handle_event(self, event: pygame.event.Event) -> str:
        if event.type == pygame.MOUSEMOTION:
            self._hovered = None
            for lvl in range(1, self._total + 1):
                if self._get_cell_rect(lvl).collidepoint(event.pos):
                    self._hovered = lvl

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for lvl in range(1, self._total + 1):
                if self._get_cell_rect(lvl).collidepoint(event.pos):
                    if lvl in self._unlocked:
                        self._selected = lvl

        if self._start_btn.handle_event(event) and self._selected is not None:
            return "start"
        if self._back_btn.handle_event(event):
            return "back"
        return ""

    def draw(self, surface: pygame.Surface) -> None:
        draw_text(surface, TXT_CHOOSE_LEVEL, FS_TITLE, C_TITLE_CLR,
                  SCREEN_WIDTH // 2, self._oy - 60, anchor="center")

        for lvl in range(1, self._total + 1):
            rect      = self._get_cell_rect(lvl)
            unlocked  = lvl in self._unlocked
            completed = lvl in self._completed
            selected  = lvl == self._selected
            hovered   = lvl == self._hovered and unlocked

            if selected: bg = C_BTN_HOV
            elif hovered: bg = (35, 80, 160)
            elif unlocked: bg = C_BTN
            else: bg = (25, 25, 40)
            pygame.draw.rect(surface, bg, rect, border_radius=14)

            bdr = C_GOLD if selected else (C_SHIP_ACCENT if unlocked else (50, 50, 70))
            pygame.draw.rect(surface, bdr, rect, 2 if not selected else 3, border_radius=14)

            if unlocked:
                draw_text(surface, str(lvl), FS_LARGE, C_WHITE, rect.centerx, rect.centery - 10, anchor="center")
                if completed:
                    # MAKSIMĀLISMS: Zīmējam skaistu ķeksīti GĀRFIKĀ, lai nav kvadrātu bugi!
                    cx, cy = rect.centerx, rect.centery + 18
                    pts = [(cx - 8, cy - 2), (cx - 2, cy + 6), (cx + 10, cy - 8)]
                    pygame.draw.lines(surface, C_GOLD, False, pts, 4)
            else:
                draw_text(surface, str(lvl), FS_MED, (60, 60, 80), rect.centerx, rect.centery - 10, anchor="center")
                draw_text(surface, TXT_LOCKED, FS_SMALL, (60, 60, 80), rect.centerx, rect.centery + 16, anchor="center")

        if self._selected is not None:
            self._start_btn.draw(surface)

        self._back_btn.draw(surface)
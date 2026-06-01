"""
Spēles loģika / Gameplay session
"""
from __future__ import annotations
import random
import math
import pygame

from entities.ship     import Ship
from entities.asteroid import Asteroid
from entities.pickup   import HealthPickup, FuelPickup
from background        import Background
from particles         import ParticleSystem
from math_tasks        import generate_task, MathTask
from ui                import HUD, TaskPopup, draw_finish_line, draw_text
from constants         import *


class GameSession:
    def __init__(self, app, cfg: dict) -> None:
        self._app    = app # Piekļuve galvenajam App (main.py)
        self._clock  = app._clock
        self._cfg    = cfg

        self._ship       = Ship()
        self._asteroids: list[Asteroid] = []
        self._pickups:   list[HealthPickup | FuelPickup] = []

        self._world_height:  float = float(cfg["world_height"])
        self._scroll_speed:  float = float(cfg["scroll_speed"])
        self._cam_offset_y:  float = float(cfg["world_height"]) 

        self._ship._y = self._cam_offset_y + SHIP_SCREEN_Y

        self._bg         = Background()
        self._particles  = ParticleSystem()
        self._hud        = HUD()
        self._popup      = TaskPopup()

        self._strikes:      int   = 0
        self._paused:       bool  = False   
        self._done:         bool  = False
        self._result:       str   = ""      
        self._lose_reason:  str   = ""

        self._hit_cooldown: float = 0.0
        self._shake_timer:  float = 0.0 

        self._math_timer:    float = random.uniform(*cfg["math_interval"])
        self._active_task:   MathTask | None = None
        self._task_time:     float = 0.0
        self._task_max:      float = float(cfg["math_time"])
        self._is_breakdown:  bool  = False   

        self._breakdown_timer: float = random.uniform(*cfg["breakdown_interval"])
        self._emergency_popup: bool = False   

        self._spawn_pickups()

    def _spawn_pickups(self) -> None:
        cfg, wh = self._cfg, self._world_height
        for _ in range(cfg["pickups_health"]):
            self._pickups.append(HealthPickup(random.randint(60, SCREEN_WIDTH - 60), random.uniform(wh * 0.10, wh * 0.88)))
        for _ in range(cfg["pickups_fuel"]):
            self._pickups.append(FuelPickup(random.randint(60, SCREEN_WIDTH - 60), random.uniform(wh * 0.10, wh * 0.88)))

    def run(self) -> dict:
        while not self._done:
            dt = min(self._clock.tick(FPS) / 1000.0, 0.05)
            self._handle_events()
            
            if self._shake_timer > 0: 
                self._shake_timer -= dt

            if not self._paused:
                self._update(dt)
            else:
                self._update_popup(dt)
                
            self._draw()
        return {"result": self._result, "reason": self._lose_reason}

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: raise SystemExit
            if self._app.handle_video_event(event): continue

            if self._paused and self._active_task:
                if self._popup.handle_key(event) == "submit":
                    self._submit_answer()
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if self._ship.is_out_of_fuel and not self._ship.emergency_used:
                    self._start_emergency_task()

    def _update(self, dt: float) -> None:
        current_scroll = self._scroll_speed
        if self._ship.is_out_of_fuel:
            current_scroll = 0.0 
        elif self._ship.fuel < LOW_FUEL_THRESHOLD:
            current_scroll = self._scroll_speed * 0.6 
            
        self._cam_offset_y -= current_scroll * dt
        self._ship._y = self._cam_offset_y + SHIP_SCREEN_Y

        if self._ship._y <= 0:
            self._result, self._done = "win", True
            return

        self._ship.update(dt)
        if not self._ship.is_out_of_fuel:
            self._particles.spawn_trail(self._ship.screen_x, SHIP_SCREEN_Y + SHIP_HEIGHT//2, C_FLAME_OUT)

        while len(self._asteroids) < self._cfg["asteroid_count"]:
            self._asteroids.append(Asteroid(random.randint(50, SCREEN_WIDTH - 50), self._cam_offset_y - random.randint(100, 400), self._cfg["asteroid_speed"]/100.0))

        for a in self._asteroids[:]:
            a.update(dt)
            if a.screen_y(self._cam_offset_y) > SCREEN_HEIGHT + 150: self._asteroids.remove(a)

        for p in self._pickups: p.update(dt)
        self._particles.update()

        if self._hit_cooldown > 0: self._hit_cooldown -= dt
        else: self._check_asteroid_collisions()
        self._check_pickup_collisions()

        self._math_timer -= dt
        if self._math_timer <= 0 and not self._paused: self._start_math_task(breakdown=False)

        self._breakdown_timer -= dt
        if self._breakdown_timer <= 0 and not self._paused: self._start_math_task(breakdown=True)

        self._check_lose_conditions()

    def _update_popup(self, dt: float) -> None:
        if self._active_task is None: return
        self._task_time -= dt
        if self._task_time <= 0 and self._popup._result == "":
            ans = self._active_task.answer
            ans_str = str(int(ans)) if float(ans).is_integer() else str(ans)
            self._popup.show_result("timeout", ans_str)
            self._handle_timeout()
        if self._popup.update(dt): self._close_popup()

    def _start_math_task(self, breakdown: bool = False) -> None:
        self._active_task  = generate_task(self._cfg["difficulty"])
        self._task_time = self._task_max = float(self._cfg["math_time"])
        self._is_breakdown, self._paused = breakdown, True
        self._popup.reset()
        if breakdown: self._breakdown_timer = random.uniform(*self._cfg["breakdown_interval"])
        else: self._math_timer = random.uniform(*self._cfg["math_interval"])

    def _start_emergency_task(self) -> None:
        self._active_task  = generate_task(min(5, self._cfg["difficulty"] + 2))
        self._task_time = self._task_max = 20.0
        self._is_breakdown = False
        self._emergency_popup, self._paused = True, True
        self._popup.reset()

    def _submit_answer(self) -> None:
        if self._active_task is None: return
        correct = self._active_task.check(self._popup.input_text)
        ans = self._active_task.answer
        ans_str = str(int(ans)) if float(ans).is_integer() else str(ans)

        if self._emergency_popup:
            if correct: self._ship.add_fuel(EMERGENCY_FUEL_AMOUNT)
            self._ship.emergency_used = True
            self._emergency_popup = False
            self._popup.show_result("correct" if correct else "wrong", "" if correct else ans_str)
            return

        if correct:
            self._popup.show_result("correct")
            if self._is_breakdown: self._ship.start_fuel_saving()
        else:
            self._popup.show_result("wrong", ans_str)
            self._handle_wrong_answer()

    def _handle_wrong_answer(self) -> None:
        self._strikes += 1
        if self._is_breakdown:
            self._ship.fuel -= BREAKDOWN_FUEL_PENALTY
            self._particles.spawn_hit(int(self._ship.screen_x), int(SHIP_SCREEN_Y), C_FUEL_PICK, PARTICLE_COUNT_PICK)

    def _handle_timeout(self) -> None: self._handle_wrong_answer()

    def _close_popup(self) -> None:
        self._active_task, self._paused = None, False
        self._popup.reset()

    def _check_asteroid_collisions(self) -> None:
        ship_rect = self._ship.get_rect()
        for ast in self._asteroids:
            if not ship_rect.colliderect(ast.get_screen_rect(self._cam_offset_y)): continue
            self._shake_timer, self._hit_cooldown = 0.4, 1.0   
            self._ship.take_damage(ast.damage_amount)
            dx, dy = self._ship.screen_x - ast.x, SHIP_SCREEN_Y - ast.screen_y(self._cam_offset_y)
            dist = math.hypot(dx, dy) or 1
            self._ship.bounce_away(dx / dist, dy / dist)
            self._particles.spawn_hit(int(self._ship.screen_x), int(SHIP_SCREEN_Y), C_SHIP_BODY, PARTICLE_COUNT_HIT)
            break

    def _check_pickup_collisions(self) -> None:
        ship_rect = self._ship.get_rect()
        for pickup in self._pickups:
            if pickup.collected: continue
            if not ship_rect.colliderect(pickup.get_screen_rect(self._cam_offset_y)): continue
            pickup.collect(self._ship)
            self._particles.spawn_pickup(int(pickup.x), int(pickup.screen_y(self._cam_offset_y)), pickup.get_particle_color(), PARTICLE_COUNT_PICK)
        self._pickups = [p for p in self._pickups if not p.collected]

    def _check_lose_conditions(self) -> None:
        if self._ship.is_out_of_health:
            self._result, self._lose_reason, self._done = "lose", TXT_NO_HEALTH, True
        elif self._strikes >= MAX_STRIKES:
            self._result, self._lose_reason, self._done = "lose", TXT_3_STRIKES, True
        elif self._ship.is_out_of_fuel and self._ship.emergency_used:
            self._result, self._lose_reason, self._done = "lose", TXT_OUT_FUEL, True

    def _draw(self) -> None:
        sx, sy = 0, 0
        if self._shake_timer > 0:
            power = int(self._shake_timer * 20)
            sx, sy = random.randint(-power, power), random.randint(-power, power)

        render_surf = self._app.logical_surface
        
        self._bg.draw(render_surf, self._cam_offset_y)
        draw_finish_line(render_surf, self._cam_offset_y, self._world_height, self._scroll_speed)

        for p in self._pickups: p.draw(render_surf, self._cam_offset_y)
        for a in self._asteroids: a.draw(render_surf, self._cam_offset_y)
        
        self._particles.draw(render_surf)
        self._ship.draw(render_surf)

        progress_ratio = max(0.0, min(1.0, (self._world_height - self._cam_offset_y) / self._world_height))
        self._hud.draw(render_surf, self._ship.health, SHIP_MAX_HEALTH, self._ship.fuel, SHIP_MAX_FUEL, self._strikes, MAX_STRIKES, not self._ship.emergency_used, progress_ratio)

        if self._ship.is_out_of_fuel and not self._ship.emergency_used:
            pulse = 155 + int(100 * math.sin(pygame.time.get_ticks() / 150))
            draw_text(render_surf, "Nospied [E] ārkārtas degvielai!", FS_MED, (pulse, pulse, 20), SCREEN_WIDTH // 2, SCREEN_HEIGHT - 90, anchor="center")

        if self._paused and self._active_task:
            self._popup.draw(render_surf, self._active_task.question, self._task_time, self._task_max, self._is_breakdown)

        self._app._render_and_scale(sx, sy)
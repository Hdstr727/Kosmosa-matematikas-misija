import pygame
import math
import random

# Pygame inicializācija
pygame.init()

# Loģiskā izšķirtspēja (spēles iekšējais izmērs)
LOGICAL_WIDTH = 1280
LOGICAL_HEIGHT = 720

# Sākotnējais loga izmērs
window_size = (LOGICAL_WIDTH, LOGICAL_HEIGHT)
screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)
pygame.display.set_caption("Kosmosa Matemātikas Misija - VERTICAL PRO")

# Loģiskā virsma (viss tiek zīmēts šeit, pēc tam mērogots uz ekrānu)
logical_surface = pygame.Surface((LOGICAL_WIDTH, LOGICAL_HEIGHT))

# Šrifti
font_main = pygame.font.SysFont("Arial", 48, bold=True)
font_ui = pygame.font.SysFont("Arial", 28, bold=True)

# Krāsas
WHITE = (255, 255, 255)
BLACK = (5, 5, 15)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (100, 150, 255)
YELLOW = (255, 200, 0)
CYAN = (50, 255, 255)

# --- KLASES ---

class Particle:
    # Daļiņu sistēma vizuālajiem efektiem
    def __init__(self, x, y, vx, vy, color, life):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.life = life
        self.max_life = life
        self.radius = random.uniform(2, 5)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.radius = max(0, self.radius - 0.1)

    def draw(self, surface):
        alpha = int((self.life / self.max_life) * 255)
        color = (*self.color[:3], alpha)
        temp_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(temp_surface, color, (self.radius, self.radius), self.radius)
        surface.blit(temp_surface, (self.x - self.radius, self.y - self.radius))

class Star:
    # Fona zvaigznes
    def __init__(self):
        self.x = random.randint(0, LOGICAL_WIDTH)
        self.y = random.randint(0, LOGICAL_HEIGHT)
        self.size = random.uniform(1, 3)
        self.brightness = random.randint(100, 255)
        self.blink_speed = random.uniform(-2, 2)

    def update(self):
        self.brightness += self.blink_speed
        if self.brightness >= 255 or self.brightness <= 100:
            self.blink_speed *= -1

    def draw(self, surface):
        # KĻŪDAS LABOJUMS: Nodrošina, ka krāsa vienmēr ir vesels skaitlis no 0 līdz 255
        b = int(max(0, min(255, self.brightness)))
        color = (b, b, b)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.size)

class Planet:
    # Mērķa planēta, kas jāsasniedz
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 60

    def draw(self, surface):
        pygame.draw.circle(surface, GREEN, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, (30, 150, 30), (int(self.x), int(self.y)), self.radius - 10, 5)
        
        # Mērķa teksts (tagad zem planētas, lai neietu ārpus ekrāna)
        text = font_ui.render("MĒRĶIS", True, WHITE)
        surface.blit(text, (self.x - text.get_width() // 2, self.y + self.radius + 10))

class Asteroid:
    # Kustīgs šķērslis
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = random.uniform(-1.5, 1.5)
        self.vy = random.uniform(-1.5, 1.5)

    def update(self):
        self.x += self.vx
        self.y += self.vy

        # Atlēkšana no ekrāna malām
        if self.x - self.radius < 0 or self.x + self.radius > LOGICAL_WIDTH:
            self.vx *= -1
        if self.y - self.radius < 0 or self.y + self.radius > LOGICAL_HEIGHT:
            self.vy *= -1

    def draw(self, surface):
        pygame.draw.circle(surface, RED, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, (150, 0, 0), (int(self.x), int(self.y)), self.radius, 3)

class Spaceship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.radius = 20
        self.hp = 100
        self.fuel = 100

    def draw(self, surface):
        # Kuģa spīdums (Glow efekts)
        glow = pygame.Surface((self.radius * 4, self.radius * 4), pygame.SRCALPHA)
        pygame.draw.circle(glow, (100, 150, 255, 100), (self.radius * 2, self.radius * 2), self.radius * 1.5)
        surface.blit(glow, (self.x - self.radius * 2, self.y - self.radius * 2))
        
        # Pats kuģis
        pygame.draw.circle(surface, BLUE, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, CYAN, (int(self.x), int(self.y)), self.radius, 2)

    def apply_impulse(self, dx, dy):
        # Spēks no "slingshot" novilkuma
        self.vx = dx * 0.05
        self.vy = dy * 0.05

    def update(self, particles):
        self.x += self.vx
        self.y += self.vy
        
        # Kosmosa berze
        self.vx *= 0.99
        self.vy *= 0.99
        
        # Dzinēja daļiņas, kad kuģis kustas
        speed = math.hypot(self.vx, self.vy)
        if speed > 1:
            particles.append(Particle(self.x, self.y, -self.vx*0.2 + random.uniform(-1,1), -self.vy*0.2 + random.uniform(-1,1), CYAN, 20))

        # Pārbauda robežas un atlec no malām
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx *= -0.8
        elif self.x + self.radius > LOGICAL_WIDTH:
            self.x = LOGICAL_WIDTH - self.radius
            self.vx *= -0.8
            
        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy *= -0.8
        elif self.y + self.radius > LOGICAL_HEIGHT:
            self.y = LOGICAL_HEIGHT - self.radius
            self.vy *= -0.8

        # Apstāšanās slieksnis
        if speed < 0.2:
            self.vx = 0
            self.vy = 0

class MathSystem:
    # Ģenerē uzdevumus atkarībā no līmeņa
    @staticmethod
    def generate_task(level):
        if level == 1:
            a = random.randint(5, 20)
            b = random.randint(1, 15)
            return f"Cik ir {a} + {b}?", str(a + b)
        elif level == 2:
            a = random.randint(2, 9)
            b = random.randint(2, 9)
            return f"Cik ir {a} * {b}?", str(a * b)
        else:
            x = random.randint(2, 10)
            a = random.randint(2, 5)
            res = a * x
            return f"Atrodi x: {a} * x = {res}", str(x)

# --- FUNKCIJAS ---

def generate_level(level_num):
    # IZMAIŅAS ŠEIT: Kuģis ir apakšā pa vidu
    ship = Spaceship(LOGICAL_WIDTH // 2, LOGICAL_HEIGHT - 100)
    
    # IZMAIŅAS ŠEIT: Planēta ir augšā pa vidu
    planet = Planet(LOGICAL_WIDTH // 2, 100)
    asteroids = []
    
    # Asteroīdi izvietoti pa visu ekrānu starp kuģi un planētu
    num_asteroids = 2 + level_num * 3
    for _ in range(num_asteroids):
        ax = random.randint(100, LOGICAL_WIDTH - 100)
        ay = random.randint(250, LOGICAL_HEIGHT - 250)
        ar = random.randint(20, 50)
        asteroids.append(Asteroid(ax, ay, ar))
        
    return ship, planet, asteroids

def create_explosion(x, y, particles, color):
    # Sprādziena vizuālais efekts
    for _ in range(30):
        vx = random.uniform(-5, 5)
        vy = random.uniform(-5, 5)
        particles.append(Particle(x, y, vx, vy, color, 30))

# --- SPĒLES MAINĪGIE ---

level = 1
ship, planet, asteroids = generate_level(level)
stars = [Star() for _ in range(100)]
particles = []

state = "AIMING"
drag_start = None
current_task_q = ""
current_task_a = ""
player_input = ""
saved_dx = 0
saved_dy = 0

is_fullscreen = False

clock = pygame.time.Clock()
running = True

# --- GALVENAIS CIKLS ---

while running:
    # 1. Notikumu apstrāde
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.VIDEORESIZE:
            if not is_fullscreen:
                window_size = (event.w, event.h)
                screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)
                
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            is_fullscreen = not is_fullscreen
            if is_fullscreen:
                screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                window_size = screen.get_size()
            else:
                window_size = (LOGICAL_WIDTH, LOGICAL_HEIGHT)
                screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)

        if state == "AIMING":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                scale_x = LOGICAL_WIDTH / window_size[0]
                scale_y = LOGICAL_HEIGHT / window_size[1]
                drag_start = (mx * scale_x, my * scale_y)
                
            elif event.type == pygame.MOUSEBUTTONUP and drag_start:
                mx, my = event.pos
                scale_x = LOGICAL_WIDTH / window_size[0]
                scale_y = LOGICAL_HEIGHT / window_size[1]
                drag_end = (mx * scale_x, my * scale_y)
                
                current_task_q, current_task_a = MathSystem.generate_task(level)
                player_input = ""
                
                saved_dx = drag_start[0] - drag_end[0]
                saved_dy = drag_start[1] - drag_end[1]
                
                state = "MATH"
                drag_start = None

        elif state == "MATH":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if player_input.strip() == current_task_a:
                        ship.apply_impulse(saved_dx, saved_dy)
                        ship.fuel -= 5
                        create_explosion(ship.x, ship.y, particles, GREEN)
                    else:
                        ship.fuel -= 15
                        create_explosion(ship.x, ship.y, particles, RED)
                        
                    state = "FLYING"
                elif event.key == pygame.K_BACKSPACE:
                    player_input = player_input[:-1]
                else:
                    if event.unicode.isdigit() or event.unicode == '-':
                        player_input += event.unicode
                        
        elif state == "GAME_OVER":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                level = 1
                ship, planet, asteroids = generate_level(level)
                ship.hp = 100
                ship.fuel = 100
                state = "AIMING"

    # 2. Fizikas atjaunināšana
    for star in stars:
        star.update()
        
    for p in particles[:]:
        p.update()
        if p.life <= 0:
            particles.remove(p)

    for ast in asteroids:
        ast.update()

    if state == "FLYING":
        ship.update(particles)
        
        # Sadursmes ar asteroīdiem
        for ast in asteroids:
            dist = math.hypot(ship.x - ast.x, ship.y - ast.y)
            if dist < ship.radius + ast.radius:
                ship.hp -= 20
                create_explosion(ship.x, ship.y, particles, RED)
                nx, ny = (ship.x - ast.x) / dist, (ship.y - ast.y) / dist
                ship.vx = nx * 5
                ship.vy = ny * 5
                ship.x += nx * 5
                ship.y += ny * 5

        # Pārbauda uzvaru
        dist_planet = math.hypot(ship.x - planet.x, ship.y - planet.y)
        if dist_planet < ship.radius + planet.radius:
            level += 1
            ship, planet, asteroids = generate_level(level)
            state = "AIMING"

        # Ja apstājies
        if ship.vx == 0 and ship.vy == 0:
            if ship.hp <= 0 or ship.fuel <= 0:
                state = "GAME_OVER"
            else:
                state = "AIMING"

    # 3. Zīmēšana
    logical_surface.fill(BLACK)

    for star in stars:
        star.draw(logical_surface)

    planet.draw(logical_surface)

    for ast in asteroids:
        ast.draw(logical_surface)
        
    for p in particles:
        p.draw(logical_surface)

    ship.draw(logical_surface)

    # Tēmēšanas līnija
    if state == "AIMING" and drag_start:
        mx, my = pygame.mouse.get_pos()
        scale_x = LOGICAL_WIDTH / window_size[0]
        scale_y = LOGICAL_HEIGHT / window_size[1]
        mouse_logical = (mx * scale_x, my * scale_y)
        
        dx = drag_start[0] - mouse_logical[0]
        dy = drag_start[1] - mouse_logical[1]
        
        pygame.draw.line(logical_surface, YELLOW, drag_start, mouse_logical, 2)
        pygame.draw.line(logical_surface, WHITE, (ship.x, ship.y), (ship.x + dx, ship.y + dy), 3)

    # Interfeiss
    ui_y = 20
    hp_text = font_ui.render(f"Dzīvība: {max(0, ship.hp)}%", True, RED if ship.hp <= 30 else WHITE)
    fuel_text = font_ui.render(f"Degviela: {max(0, ship.fuel)}%", True, YELLOW if ship.fuel <= 30 else WHITE)
    lvl_text = font_ui.render(f"Līmenis: {level}", True, CYAN)
    
    logical_surface.blit(hp_text, (20, ui_y))
    logical_surface.blit(fuel_text, (20, ui_y + 40))
    logical_surface.blit(lvl_text, (LOGICAL_WIDTH - 200, ui_y))

    # Matemātikas logs
    if state == "MATH":
        overlay = pygame.Surface((LOGICAL_WIDTH, LOGICAL_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        logical_surface.blit(overlay, (0, 0))
        
        q_surf = font_main.render(current_task_q, True, WHITE)
        a_surf = font_main.render(f"Tava atbilde: {player_input}_", True, GREEN)
        hint_surf = font_ui.render("Ievadi skaitli un spied ENTER", True, (200, 200, 200))
        
        logical_surface.blit(q_surf, (LOGICAL_WIDTH//2 - q_surf.get_width()//2, LOGICAL_HEIGHT//2 - 80))
        logical_surface.blit(a_surf, (LOGICAL_WIDTH//2 - a_surf.get_width()//2, LOGICAL_HEIGHT//2))
        logical_surface.blit(hint_surf, (LOGICAL_WIDTH//2 - hint_surf.get_width()//2, LOGICAL_HEIGHT//2 + 60))

    # Zaudējuma logs
    if state == "GAME_OVER":
        overlay = pygame.Surface((LOGICAL_WIDTH, LOGICAL_HEIGHT), pygame.SRCALPHA)
        overlay.fill((50, 0, 0, 200))
        logical_surface.blit(overlay, (0, 0))
        
        go_surf = font_main.render("MISIJA IZGĀZUSIES", True, RED)
        r_surf = font_ui.render("Spied 'R', lai mēģinātu vēlreiz", True, WHITE)
        
        logical_surface.blit(go_surf, (LOGICAL_WIDTH//2 - go_surf.get_width()//2, LOGICAL_HEIGHT//2 - 50))
        logical_surface.blit(r_surf, (LOGICAL_WIDTH//2 - r_surf.get_width()//2, LOGICAL_HEIGHT//2 + 20))

    # 4. Mērogošana
    scaled_surface = pygame.transform.smoothscale(logical_surface, window_size)
    screen.blit(scaled_surface, (0, 0))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
import pygame
import math
import random


pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kosmosa matemātikas misija")
font = pygame.font.SysFont(None, 36)


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (100, 150, 255)
YELLOW = (255, 255, 0)



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
        pygame.draw.circle(surface, BLUE, (int(self.x), int(self.y)), self.radius)
        pygame.draw.rect(surface, RED, (10, 10, self.hp * 2, 20))
        pygame.draw.rect(surface, YELLOW, (10, 40, self.fuel * 2, 20))

    def apply_impulse(self, dx, dy):
        self.vx = dx * 0.1
        self.vy = dy * 0.1

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.98
        self.vy *= 0.98
    
        if abs(self.vx) < 0.1 and abs(self.vy) < 0.1:
            self.vx = 0
            self.vy = 0

class Asteroid:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, surface):
        pygame.draw.circle(surface, RED, (self.x, self.y), self.radius)

class MathTask:
    def __init__(self):
        
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        self.question = f"Cik ir {a} + {b}?"
        self.answer = str(a + b)



ship = Spaceship(100, HEIGHT // 2)
asteroids = [Asteroid(400, 300, 40), Asteroid(600, 150, 30), Asteroid(500, 450, 50)]

state = "AIMING"  
drag_start = None
drag_end = None
current_task = None
player_input = ""

clock = pygame.time.Clock()
running = True

while running:
    screen.fill(BLACK)

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if state == "AIMING":
            if event.type == pygame.MOUSEBUTTONDOWN:
                drag_start = event.pos
            elif event.type == pygame.MOUSEBUTTONUP and drag_start:
                drag_end = event.pos
                
                current_task = MathTask()
                player_input = ""
                state = "MATH_QUESTION"

        elif state == "MATH_QUESTION":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    
                    if player_input == current_task.answer:
                        
                        dx = drag_start[0] - drag_end[0]
                        dy = drag_start[1] - drag_end[1]
                        ship.apply_impulse(dx, dy)
                        ship.fuel -= 10
                    else:
                        
                        ship.fuel -= 20
                    state = "FLYING"
                    drag_start = None
                elif event.key == pygame.K_BACKSPACE:
                    player_input = player_input[:-1]
                else:
                    player_input += event.unicode

   
    if state == "FLYING":
        ship.update()
        
        
        for ast in asteroids:
            dist = math.hypot(ship.x - ast.x, ship.y - ast.y)
            if dist < ship.radius + ast.radius:
                ship.hp -= 10 
                ship.vx *= -1  
                ship.vy *= -1
                ship.x += ship.vx * 2 
        
        
        if ship.vx == 0 and ship.vy == 0:
            state = "AIMING"

    
    
   
    if state == "AIMING" and drag_start:
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.line(screen, WHITE, drag_start, mouse_pos, 2)
        
    for ast in asteroids:
        ast.draw(screen)
    ship.draw(screen)

    
    if state == "MATH_QUESTION":
       
        s = pygame.Surface((WIDTH, HEIGHT))
        s.set_alpha(128)
        s.fill(BLACK)
        screen.blit(s, (0,0))
        
        
        q_text = font.render(current_task.question, True, WHITE)
        ans_text = font.render("Atbilde: " + player_input, True, GREEN)
        screen.blit(q_text, (WIDTH//2 - 100, HEIGHT//2 - 50))
        screen.blit(ans_text, (WIDTH//2 - 100, HEIGHT//2))

    
    if ship.hp <= 0 or ship.fuel <= 0:
        game_over_text = font.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (WIDTH//2 - 100, HEIGHT//2))
        state = "GAME_OVER"

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
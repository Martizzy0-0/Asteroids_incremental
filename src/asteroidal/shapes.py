import pygame
import random
from asteroidal.constants import *


# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...]

    def __init__(self, x: float, y: float, radius: float) -> None:
        if self.containers:
            super().__init__(*self.containers)
        else:
            super().__init__()

        self.position: pygame.Vector2 = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen: pygame.Surface) -> None:
        # must override
        pass

    def update(self, dt: float) -> None:
        # must override
        pass

    def collides_with(self, other):
        if other.position.distance_to(self.position) < self.radius + other.radius:
            return True

# Player Class
class Player(CircleShape):
    rotation = 0
    shot_cooldown = 0
    
    def __init__(self, x, y, PLAYER_RADIUS):
        super().__init__(x, y, PLAYER_RADIUS)
        
    def draw(self, screen) -> None:
        __polygons = self.triangle()
        pygame.draw.polygon(screen, "white", __polygons, width=LINE_WIDTH)
        
    
    # draw player shape
    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def rotate(self, dt: float):
        self.rotation += dt * PLAYER_TURN_SPEED
        
    def move(self, dt: float):
        unit_vector = pygame.Vector2(0,1)
        rotated_vector = unit_vector.rotate(self.rotation)
        speedy_rotated_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += speedy_rotated_vector
    
    def shoot(self):
            shot = Shot(self.position.x, self.position.y)
            shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED      
    
    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        self.shot_cooldown -= dt

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            if self.shot_cooldown > 0:
                return
            else:
                self.shoot()
                self.shot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "white", self.position, SHOT_RADIUS)
    
    def update(self, dt: float) -> None:
        self.position += self.velocity * dt

class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
        self.x = x
        self.y = y
    
    def draw(self, screen: pygame.Surface):        
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)
    
    def update(self, dt: float):
        self.position += self.velocity * dt
    
    def split(self):
        self.kill()
        
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            rand_angle = random.uniform(20,50)
            
            asterotation_1 = self.velocity.rotate(rand_angle)
            asterotation_2 = self.velocity.rotate(-rand_angle)
            
            asteradius = self.radius - ASTEROID_MIN_RADIUS
            
            asteroid_1 = Asteroid(self.position.x, self.position.y, asteradius)
            asteroid_2 = Asteroid(self.position.x, self.position.y, asteradius)
            
            asteroid_1.velocity = asterotation_1 * 1.2
            asteroid_2.velocity = asterotation_2 * 1.2
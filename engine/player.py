import pygame
from engine.actor import Actor

UNIT_SIZE = 100

class Player(Actor):
    def __init__(self, x, y, texture):
        super().__init__(x, y)
        self.size = 1.0
        self.texture = texture
        self.speed = 0.1
        self.health = 100
        self.max_health = 100
        self.is_dead = False

    def take_damage(self, amount):
        if not self.is_dead:
            self.health -= amount
            if self.health <= 0:
                self.health = 0
                self.is_dead = True

    def move(self, x, y):
        self.x += x
        self.y += y

    def draw(self, screen):
        pixel_size = int(self.size * UNIT_SIZE)
        
        frame = self.get_current_frame()
        if frame is None:
            frame = self.texture
            
        scaled_texture = pygame.transform.scale(frame, (pixel_size, pixel_size))
        screen.blit(scaled_texture, (self.x * UNIT_SIZE, self.y * UNIT_SIZE))

import pygame
from engine.actor import Actor

UNIT_SIZE = 100

class Tile(Actor):
    def __init__(self, x, y, image, is_solid=False, disappears_on=None):
        super().__init__(x, y)
        self.size = 1.0
        self.image = pygame.transform.scale(image, (UNIT_SIZE, UNIT_SIZE))
        self.is_solid = is_solid
        self.disappears_on = disappears_on
        self.is_active = True
        
    def interact(self, entity):
        if not self.is_active or entity is None:
            return

        tile_rect = pygame.Rect(self.x * UNIT_SIZE, self.y * UNIT_SIZE, UNIT_SIZE, UNIT_SIZE)
        
        entity_pixel_size = getattr(entity, 'size', 1.0) * UNIT_SIZE
        entity_rect = pygame.Rect(entity.x * UNIT_SIZE, entity.y * UNIT_SIZE, entity_pixel_size, entity_pixel_size)
        
        if tile_rect.colliderect(entity_rect):
            if self.disappears_on and isinstance(entity, self.disappears_on):
                self.is_active = False
                self.is_solid = False

    def update(self):
        pass

    def draw(self, screen):
        if self.is_active:
            screen.blit(self.image, (self.x * UNIT_SIZE, self.y * UNIT_SIZE))
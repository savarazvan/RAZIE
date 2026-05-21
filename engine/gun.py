import pygame
from engine.actor import Actor

try:
    from engine.player import UNIT_SIZE
except ImportError:
    UNIT_SIZE = 100

class Bullet(Actor):
    def __init__(self, x, y, dx, dy, speed=0.3, game_map=None, actor_manager=None, owner=None):
        super().__init__(x, y)
        self.dx = dx
        self.dy = dy
        self.speed = speed
        self.life = 60
        self.is_dead = False
        self.size = 0.2
        self.game_map = game_map
        self.actor_manager = actor_manager
        self.owner = owner

    def update(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
        
        if self.game_map:
            eps = 0.001
            corners = [
                (self.x + eps, self.y + eps),
                (self.x + self.size - eps, self.y + eps),
                (self.x + eps, self.y + self.size - eps),
                (self.x + self.size - eps, self.y + self.size - eps)
            ]
            for cx, cy in corners:
                if self.game_map.is_out_of_bounds(cx, cy):
                    self.is_dead = True
                    break
                tile = self.game_map.get_tile_at(cx, cy)
                if tile and getattr(tile, 'is_solid', False):
                    self.is_dead = True
                    break

        if not self.is_dead and self.actor_manager:
            for actor in self.actor_manager.actors:
                if actor is self or actor is self.owner:
                    continue
                if getattr(actor, 'is_dead', False):
                    continue
                if type(actor).__name__ not in ['Player', 'Enemy']:
                    continue
                
                actor_size = getattr(actor, 'size', 1.0)
                if (self.x < actor.x + actor_size and 
                    self.x + self.size > actor.x and 
                    self.y < actor.y + actor_size and 
                    self.y + self.size > actor.y):
                    
                    if hasattr(actor, 'take_damage'):
                        actor.take_damage(20)
                    else:
                        actor.is_dead = True
                    self.is_dead = True
                    break

        self.life -= 1
        if self.life <= 0:
            self.is_dead = True

    def draw(self, screen):
        pixel_size = int(self.size * UNIT_SIZE)
        center_x = int((self.x + self.size / 2) * UNIT_SIZE)
        center_y = int((self.y + self.size / 2) * UNIT_SIZE)
        radius = pixel_size // 2
        pygame.draw.circle(screen, (0, 0, 0), (center_x, center_y), radius)

class Gun:
    def __init__(self, actor_manager):
        self.actor_manager = actor_manager
        self.cooldown = 15
        self.timer = 0

    def handle_input(self, keys, origin_x, origin_y, game_map=None, owner=None):
        if self.timer > 0:
            self.timer -= 1
            return
            
        dx, dy = 0, 0
        if keys[pygame.K_UP]:
            dy = -1
        elif keys[pygame.K_DOWN]:
            dy = 1
        if keys[pygame.K_LEFT]:
            dx = -1
        elif keys[pygame.K_RIGHT]:
            dx = 1
            
        if dx != 0 or dy != 0:
            bullet = Bullet(origin_x + 0.4, origin_y + 0.4, dx, dy, game_map=game_map, actor_manager=self.actor_manager, owner=owner)
            self.actor_manager.add_actor(bullet)
            self.timer = self.cooldown

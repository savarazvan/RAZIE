import pygame
import math
from engine.actor import Actor
from engine.gun import Bullet

try:
    from engine.player import UNIT_SIZE
except ImportError:
    UNIT_SIZE = 100

class Enemy(Actor):
    def __init__(self, x, y, player, game_map, actor_manager):
        super().__init__(x, y)
        self.player = player
        self.game_map = game_map
        self.actor_manager = actor_manager
        self.speed = 0.05
        self.size = 1.0
        self.shoot_cooldown = 60
        self.shoot_timer = 0
        self.is_dead = False

    def can_move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy
        eps = 0.001
        corners = [
            (new_x + eps, new_y + eps),
            (new_x + self.size - eps, new_y + eps),
            (new_x + eps, new_y + self.size - eps),
            (new_x + self.size - eps, new_y + self.size - eps)
        ]
        for cx, cy in corners:
            if self.game_map and self.game_map.is_out_of_bounds(cx, cy):
                return False
            tile = self.game_map.get_tile_at(cx, cy)
            if tile and getattr(tile, 'is_solid', False):
                return False
        return True

    def update(self):
        if not self.player:
            return

        dx = self.player.x - self.x
        dy = self.player.y - self.y
        dist = math.hypot(dx, dy)
        
        if dist > 0:
            dir_x = dx / dist
            dir_y = dy / dist
            
            move_x = dir_x * self.speed
            move_y = dir_y * self.speed
            
            if self.can_move(move_x, 0):
                self.x += move_x
            if self.can_move(0, move_y):
                self.y += move_y
            self.shoot_timer -= 1
            if self.shoot_timer <= 0:
                self.shoot_timer = self.shoot_cooldown
                bullet = Bullet(self.x + self.size/2 - 0.1, self.y + self.size/2 - 0.1, dir_x, dir_y, speed=0.15, game_map=self.game_map, actor_manager=self.actor_manager, owner=self)
                self.actor_manager.add_actor(bullet)

    def draw(self, screen):
        pixel_x = int(self.x * UNIT_SIZE)
        pixel_y = int(self.y * UNIT_SIZE)
        pixel_size = int(self.size * UNIT_SIZE)
        
        frame = self.get_current_frame()
        if frame:
            scaled = pygame.transform.scale(frame, (pixel_size, pixel_size))
            screen.blit(scaled, (pixel_x, pixel_y))
        else:
            pygame.draw.rect(screen, (255, 0, 0), (pixel_x, pixel_y, pixel_size, pixel_size))

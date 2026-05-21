import pygame

from engine.actor_manager import ActorManager
from engine.asset_loader import AssetLoader
from engine.hud_manager import HUDManager
from engine.player import Player
from engine.map import Map
from engine.gun import Gun


class GameEngine:
    
    player: Player = None
    map: Map = None
    elapsed_time = 0.0

    def __init__(self, width=1200, height=900, title="My Game Engine", assets_path="assets"):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = True
        self.asset_loader = AssetLoader(base_path=assets_path)
        self.hud_manager = HUDManager()
        self.actor_manager = ActorManager()
        self.gun = Gun(self.actor_manager)
    
    def handle_input(self):
        if not self.player:
            return
            
        keys = pygame.key.get_pressed()
        
        def can_move(dx, dy):
            new_x = self.player.x + dx
            new_y = self.player.y + dy
            size = getattr(self.player, 'size', 1.0)
            eps = 0.001
            corners = [
                (new_x + eps, new_y + eps),
                (new_x + size - eps, new_y + eps),
                (new_x + eps, new_y + size - eps),
                (new_x + size - eps, new_y + size - eps)
            ]
            for cx, cy in corners:
                if self.map and self.map.is_out_of_bounds(cx, cy):
                    return False
                tile = self.map.get_tile_at(cx, cy)
                if tile and getattr(tile, 'is_solid', False):
                    return False
            return True

        if keys[pygame.K_a] and can_move(-self.player.speed, 0): 
            self.player.move(-self.player.speed, 0)
        if keys[pygame.K_d] and can_move(self.player.speed, 0): 
            self.player.move(self.player.speed, 0)
        if keys[pygame.K_s] and can_move(0, self.player.speed): 
            self.player.move(0, self.player.speed)
        if keys[pygame.K_w] and can_move(0, -self.player.speed): 
            self.player.move(0, -self.player.speed)

        if self.player:
            self.gun.handle_input(keys, self.player.x, self.player.y, self.map, owner=self.player)

    def base_tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        if self.player and getattr(self.player, 'is_dead', False):
            self.player = None

        if self.player:
            self.elapsed_time += self.clock.get_time() / 1000.0

        self.hud_manager.clear_elements()
        self.hud_manager.add_text(f"Time: {int(self.elapsed_time)}s", (10, 10))
        
        if self.player:
            self.hud_manager.add_text(f"Health: {self.player.health}", (10, 50))
        else:
            self.hud_manager.add_text("Health: 0 (DEAD)", (10, 50))

        self.actor_manager.update()
        
        for actor in list(self.actor_manager.actors):
            if getattr(actor, 'is_dead', False):
                self.actor_manager.remove_actor(actor)

        self.handle_input()

        if self.map:
            self.map.check_interactions(self.player)

        self.screen.fill((30, 30, 30))
        for actor in self.actor_manager.actors:
            actor.draw(self.screen)
        
        self.hud_manager.draw(self.screen)
        pygame.display.flip()


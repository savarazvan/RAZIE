import random
import time
from pathlib import Path
from engine.engine import GameEngine
from engine.player import Player
from engine.map import Map
from engine.enemy import Enemy


def load_textures():
    my_game.asset_loader.load_texture("stone", "stone.jpg")
    my_game.asset_loader.load_texture("sand", "sand.jpg")
    
    p_path = "player/"
    my_game.asset_loader.load_texture("idle_down", p_path + "idledown.png")
    my_game.asset_loader.load_texture("idle_up", p_path + "idleup.png")
    my_game.asset_loader.load_texture("idle_left", p_path + "idleleft.png")
    my_game.asset_loader.load_texture("idle_right", p_path + "idleright.png")
    
    my_game.asset_loader.load_texture("walk_down_1", p_path + "walkdown1.png")
    my_game.asset_loader.load_texture("walk_down_2", p_path + "walkdown2.png")
    my_game.asset_loader.load_texture("walk_up_1", p_path + "walkup1.png")
    my_game.asset_loader.load_texture("walk_up_2", p_path + "walkup2.png")
    my_game.asset_loader.load_texture("walk_left_1", p_path + "left1.png")
    my_game.asset_loader.load_texture("walk_left_2", p_path + "left2.png")
    my_game.asset_loader.load_texture("walk_right_1", p_path + "right1.png")
    my_game.asset_loader.load_texture("walk_right_2", p_path + "right2.png")

    e_path = "enemy/"
    my_game.asset_loader.load_texture("e_down_1", e_path + "down1.png")
    my_game.asset_loader.load_texture("e_down_2", e_path + "down2.png")
    my_game.asset_loader.load_texture("e_up_1", e_path + "up1.png")
    my_game.asset_loader.load_texture("e_up_2", e_path + "up2.png")
    my_game.asset_loader.load_texture("e_left_1", e_path + "left1.png")
    my_game.asset_loader.load_texture("e_left_2", e_path + "left2.png")
    my_game.asset_loader.load_texture("e_right_1", e_path + "right1.png")
    my_game.asset_loader.load_texture("e_right_2", e_path + "right2.png")

my_game = GameEngine(assets_path=Path(__file__).parent / "assets")

load_textures()
last_check_time = time.time()

def check_for_npcs(number, interval):
    global last_check_time
    current_time = time.time()
    if current_time - last_check_time >= interval:
        last_check_time = current_time
        if sum(1 for a in my_game.actor_manager.actors if isinstance(a, Enemy)) >= number:
            return
            
        rows = len(level_grid)
        cols = len(level_grid[0])
        spawn_points = []
        for r in range(rows):
            for c in range(cols):
                if (r == 0 or r == rows - 1 or c == 0 or c == cols - 1) and level_grid[r][c] == 0:
                    spawn_points.append((c, r))
        
        if spawn_points:
            sx, sy = random.choice(spawn_points)
            new_enemy = Enemy(sx, sy, my_game.player, my_game.map, my_game.actor_manager)
            
            new_enemy.idle_down = [my_game.asset_loader.get_texture("e_down_1")]
            new_enemy.idle_up = [my_game.asset_loader.get_texture("e_up_1")]
            new_enemy.idle_left = [my_game.asset_loader.get_texture("e_left_1")]
            new_enemy.idle_right = [my_game.asset_loader.get_texture("e_right_1")]

            new_enemy.frames_bottom = [my_game.asset_loader.get_texture("e_down_1"), my_game.asset_loader.get_texture("e_down_2")]
            new_enemy.frames_top = [my_game.asset_loader.get_texture("e_up_1"), my_game.asset_loader.get_texture("e_up_2")]
            new_enemy.frames_left = [my_game.asset_loader.get_texture("e_left_1"), my_game.asset_loader.get_texture("e_left_2")]
            new_enemy.frames_right = [my_game.asset_loader.get_texture("e_right_1"), my_game.asset_loader.get_texture("e_right_2")]

            my_game.actor_manager.add_actor(new_enemy)
    


level_grid = [
    [1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1],
]

tile_config = {
    0: {'image': my_game.asset_loader.get_texture("sand"), 'is_solid': False, 'disappears_on': None},
    1: {'image': my_game.asset_loader.get_texture("stone"), 'is_solid': True, 'disappears_on': None}
}

game_map = Map(0, 0)
game_map.load_from_grid(level_grid, tile_config)
my_game.actor_manager.add_actor(game_map)


hero = Player(1, 1, my_game.asset_loader.get_texture("idle_down"))

hero.idle_down = [my_game.asset_loader.get_texture("idle_down")]
hero.idle_up = [my_game.asset_loader.get_texture("idle_up")]
hero.idle_left = [my_game.asset_loader.get_texture("idle_left")]
hero.idle_right = [my_game.asset_loader.get_texture("idle_right")]

hero.frames_bottom = [my_game.asset_loader.get_texture("walk_down_1"), my_game.asset_loader.get_texture("idle_down"), my_game.asset_loader.get_texture("walk_down_2"), my_game.asset_loader.get_texture("idle_down")]
hero.frames_top = [my_game.asset_loader.get_texture("walk_up_1"), my_game.asset_loader.get_texture("idle_up"), my_game.asset_loader.get_texture("walk_up_2"), my_game.asset_loader.get_texture("idle_up")]
hero.frames_left = [my_game.asset_loader.get_texture("walk_left_1"), my_game.asset_loader.get_texture("walk_left_2")]
hero.frames_right = [my_game.asset_loader.get_texture("walk_right_1"), my_game.asset_loader.get_texture("walk_right_2")]

my_game.actor_manager.add_actor(hero)
my_game.player = hero
my_game.map = game_map

start_game_time = time.time()

while my_game.running:
    my_game.base_tick()
    my_game.clock.tick(60)
    
    elapsed = time.time() - start_game_time
    max_enemies = 1 + int(elapsed / 2)
    spawn_interval = max(0.5, 3.0 - (elapsed / 10.0))
    
    check_for_npcs(max_enemies, spawn_interval)

# RAZIE

RAZIE is a 2D game engine based on Pygame. In order to demonstrate its capabilities, a simple game is included in which the player must survive endless waves of enemies as much as possible.

## Custom framework

A lightweight engine built on top of Pygame is responsible for rendering, asset management and input handling. It consists of the following components:

  - `ActorManager`: A base class that handles the lifecycle of in-game actors such as the player, map or the enemies.
  - `AssetLoader`: A class responsible for loading all the asset files, which in this iteration consists of textures.
  - `HudManager`: A class that draws heads up display (HUD) elements on screen.
  - `GameEngine`: The core game logic, featuring the main loop.

## Implementation Details (`main.py`)

The `main.py` file is the implementation of the engine itself (found in the engine folder)

1. **Asset Loading (`load_textures`):** Preloads all environment textures and player animations using the `AssetLoader`.
2. **Map Generation:** Defines the layout of the level by thea means of a matrix (`level_grid`) where `1` represents solid stone walls and `0` represents walkable sand. This is parsed by the `Map` class.
3. **Player Initialization:** Instantiates the `Player` (child class of `ActorManager`), positions it to the origin point of the engine's internally coordinates system and assigns the loaded texture frames for each directional state (idle and walking) .
4. **Enemy Spawning Logic (`check_for_npcs`):** 
   - Checks empty boundary tiles (`0`s on the edges of the grid), which are used as spawn points.
   - Instantiates `Enemy` objects with their respective animation frames.
5. **Main Game Loop:**
   - Runs at a targeted 60 FPS.
   - Calls the engine's `base_tick()` to update in-game logic.
   - The game features a dynamic difficulty, scaled with time. It increases the maximum enemies which can be present at once (`max_enemies`) and decreases the `spawn_interval` as more time passes..

## Setup and Requirements

The game requires Python 3.x and the pygame specific dependency is found in `engine/requirements.txt`.

```bash
# Install dependencies
pip install -r engine/requirements.txt

# Run the game
python main.py
```

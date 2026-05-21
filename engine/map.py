from engine.actor import Actor
from engine.tile import Tile

class Map(Actor):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.tiles = []

    def load_from_grid(self, grid, tile_mapping):
        self.tiles = []
        for row_idx, row in enumerate(grid):
            tile_row = []
            for col_idx, tile_id in enumerate(row):
                if tile_id in tile_mapping:
                    config = tile_mapping[tile_id]
                    tile_x = self.x + col_idx
                    tile_y = self.y + row_idx
                    
                    tile = Tile(
                        x=tile_x,
                        y=tile_y,
                        image=config['image'],
                        is_solid=config.get('is_solid', False),
                        disappears_on=config.get('disappears_on', None)
                    )
                    tile_row.append(tile)
                else:
                    tile_row.append(None)
            self.tiles.append(tile_row)

    def update(self):
        pass

    def draw(self, screen):
        for row in self.tiles:
            for tile in row:
                if tile:
                    tile.draw(screen)

    def check_interactions(self, entity):
        for row in self.tiles:
            for tile in row:
                if tile:
                    tile.interact(entity)

    def is_out_of_bounds(self, x, y):
        import math
        col = math.floor(x - self.x)
        row = math.floor(y - self.y)
        return not (0 <= row < len(self.tiles) and 0 <= col < len(self.tiles[row]))

    def get_tile_at(self, x, y):
        import math
        col = math.floor(x - self.x)
        row = math.floor(y - self.y)
        if 0 <= row < len(self.tiles) and 0 <= col < len(self.tiles[row]):
            return self.tiles[row][col]
        return None
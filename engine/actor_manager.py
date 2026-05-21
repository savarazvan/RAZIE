class ActorManager:
    def __init__(self):
        self.actors = []
        self.grid = {}
        
    def add_actor(self, actor):
        self.actors.append(actor)

    def remove_actor(self, actor):
        if actor in self.actors:
            self.actors.remove(actor)
            return True
        return False

    def update(self):
        self.grid.clear()
        for actor in self.actors:
            actor.update()
            
            coord = (int(actor.x), int(actor.y))
            if coord not in self.grid:
                self.grid[coord] = []
            self.grid[coord].append(actor)

    def get_actors_at(self, x, y):
        return self.grid.get((int(x), int(y)), [])
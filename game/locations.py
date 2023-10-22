# locations.py module
from game.game_elements import Location
from game.location_connections import Door


class Cell(Location):
    def __init__(self, game):
        name = "cell"
        description = "A dimly lit prison cell."
        super().__init__(game, name, description)
        cell_door = Door(game, name="door", description="A heavy wooden cell door.")
        dungeon = Dungeon(game)
        cell_door.connected_locations.extend([self, dungeon])
        self.location_connections.append(cell_door)
        dungeon.location_connections.append(cell_door)


class Dungeon(Location):
    def __init__(self, game):
        name = "dungeon"
        description = "A prison dungeon."
        super().__init__(game, name, description)

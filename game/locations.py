# locations.py module
from game.game_elements import Location
from game.location_connections import Door


class Cell(Location):
    def __init__(self):
        name = "cell"
        description = "A dimly lit prison cell."
        super().__init__(name, description)
        cell_door = Door(name="door", description="A heavy wooden cell door.")
        dungeon = Dungeon()
        cell_door.connected_locations.extend([self, dungeon])
        self.location_connections.append(cell_door)
        dungeon.location_connections.append(cell_door)


class Dungeon(Location):
    def __init__(self):
        name = "dungeon"
        description = "A prison dungeon."
        super().__init__(name, description)

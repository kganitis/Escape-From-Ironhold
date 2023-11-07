# locations.py module
from .game_object import *
from .outcomes import *


class Location(GameObject, Accessible, ABC):
    def __init__(self, name, description, parent):
        super().__init__(name, description, parent)
        self.location_connections = {}  # All the location connections to this location

    @property
    # All the items that can be found in this location
    def items(self):
        return self.children

    def add_connection(self, location_connection):
        for location in location_connection.connected_locations:
            self.location_connections[location] = location_connection

    @property
    def connections(self):
        return list(self.location_connections.values())

    def get_connection_to(self, location):
        return self.location_connections.get(location)


class Cell(Location):
    def __init__(self, parent):
        name = "cell"
        description = "A dimly lit prison cell."
        super().__init__(name, description, parent)


class Dungeon(Location):
    def __init__(self, parent):
        name = "dungeon"
        description = "A prison dungeon."
        super().__init__(name, description, parent)


class Courtyard(Location):
    def __init__(self, parent):
        name = "courtyard"
        description = "Ironhold prison's courtyard."
        super().__init__(name, description, parent)

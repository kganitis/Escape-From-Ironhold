# game_elements.py module
from game.properties import *


# Define a common parent class for all game elements (locations, items, actions etc.)
class GameElement(ABC):
    def __init__(self, game, name, description):
        self.game = game
        self.name = name
        self.description = description
        game.game_elements_repository[name] = self  # every game element created is added to the repository

    def __str__(self):
        return self.name

    def describe(self):
        pass


# All game elements are further represented by abstract classes
class Character(GameElement, ABC):
    def __init__(self, game, name, description):
        super().__init__(game, name, description)


class Item(GameElement, ABC):
    def __init__(self, game, name, description):
        super().__init__(game, name, description)


class Location(GameElement, Accessible, ABC):
    def __init__(self, game, name, description):
        super().__init__(game, name, description)
        self.items = []  # All the items that can be found in this location
        self.location_connections = []  # All the location connections for this location

    def connected_locations(self):
        return [location for connection in self.location_connections for location in connection if location != self]

    def get_connection_to(self, location):
        connection = None
        for location_connection in self.location_connections:
            for connected_location in location_connection.connected_locations:
                if connected_location == location:
                    connection = location_connection
        return connection

    def go(self):
        current_location = self.game.current_location
        new_location = self
        connection_to_current_location = new_location.get_connection_to(current_location)

        if new_location == current_location:
            # return f"Already in {new_location}", FAIL
            return f"Already in this location", FAIL

        if not connection_to_current_location:
            # return f"Can't access {new_location} from {current_location}", FAIL
            return f"Can't access that from your current location", FAIL

        blocked = connection_to_current_location.is_blocked()
        if blocked:
            return blocked

        self.game.current_location = new_location
        return f"Accessed the {new_location}", SUCCESS


class LocationConnection(GameElement, ABC):
    def __init__(self, game, name, description):
        super().__init__(game, name, description)
        self.connected_locations = []
        self.items = []  # Items found in this location connection

    def is_blocked(self):
        return f"{self} is blocked", FAIL

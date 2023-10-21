# game_elements.py module
from abc import ABC

from game.properties import Accessible


# Define a common parent class for all game elements (locations, items, actions etc.)
class GameElement(ABC):
    def __init__(self, name, description):
        self.name = name
        self.description = description
        from game.game import Game
        Game().update_game_elements_repository(self)  # add every game element created in the repository

    def __str__(self):
        return self.name

    def describe(self):
        print(self.description)


# All game elements are further represented by abstract classes
class Player(GameElement, ABC):
    def __init__(self, name, description):
        super().__init__(name, description)


class Item(GameElement, ABC):
    def __init__(self, name, description):
        super().__init__(name, description)


class Location(GameElement, Accessible, ABC):
    def __init__(self, name, description):
        super().__init__(name, description)
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
        from game.game import Game
        current_location = Game().current_location
        connection_to_current_location = self.get_connection_to(current_location)
        if not connection_to_current_location:
            outcome = f"Can't access {self} from {current_location}"
        else:
            blocked = connection_to_current_location.is_blocked()
            if blocked:
                outcome = blocked
            else:
                Game().current_location = self
                outcome = f"Accessed the {self}"
        return outcome


class LocationConnection(GameElement, ABC):
    def __init__(self, name, description):
        super().__init__(name, description)
        self.connected_locations = []
        self.items = []  # Items found to this location connection

    def is_blocked(self):
        outcome = f"{self} is blocked"
        return outcome

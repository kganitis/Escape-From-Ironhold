# game_elements.py module
from abc import ABC


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


class Location(GameElement, ABC):
    def __init__(self, name, description, items=None):
        super().__init__(name, description)
        if items is None:
            items = []
        self.items = items  # All the items that can be found in this location

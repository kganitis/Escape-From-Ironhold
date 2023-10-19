# game_elements.py module
from abc import ABC, abstractmethod

from game.result import Result

# A repository to hold every game element created
# Using the element's name, we'll be able to retrieve the instance of the game element
# Useful for matching command arguments to actual instances of game elements
game_elements_repository = {}


def update_game_elements_repository(game_element):
    game_elements_repository[game_element.name] = game_element


def get_game_element(name):
    return game_elements_repository[name]


# Define a common parent class for all game elements (locations, items, actions etc.)
class GameElement(ABC):
    def __init__(self, name, description):
        self.name = name
        self.description = description
        update_game_elements_repository(self)  # add every game element created in the repository

    def __str__(self):
        return self.name

    def describe(self):
        print(self.description)


# All game elements are further represented by abstract classes
class Player(GameElement, ABC):
    def __init__(self, name, description):
        super().__init__(name, description)
        self.inventory = []  # Initialize an empty inventory for the player


class Item(GameElement, ABC):
    def __init__(self, name, description):
        super().__init__(name, description)


class Location(GameElement, ABC):
    def __init__(self, name, description, items=None):
        super().__init__(name, description)
        if items is None:
            items = []
        self.items = items  # All the items that can be found in this location


class Action(GameElement, ABC):
    def __init__(self, name, description):
        super().__init__(name, description)

    @abstractmethod
    def execute(self):
        pass

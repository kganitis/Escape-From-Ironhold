# character.py module
from game.game_elements import Character, GameElement
from game.items import LockPick


class Inventory(GameElement):
    def __init__(self, game):
        name = "inventory"
        description = "Your inventory of items."
        super().__init__(game, name, description)
        self.items = []

    def add(self, item):
        self.items.append(item)


class Hero(Character):
    def __init__(self, game):
        name = "Hero"
        description = "A brave hero trying to escape from the Ironhold prison."
        super().__init__(game, name, description)
        self.inventory = Inventory(game)
        self.inventory.add(LockPick(game))

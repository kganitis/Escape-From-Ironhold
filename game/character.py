# character.py module
from game.game_elements import Character, GameElement


class Inventory(GameElement):
    def __init__(self, game, parent):
        name = "inventory"
        description = "Your inventory of items."
        super().__init__(game, name, description, parent)
        self.items = []

    def add(self, item):
        self.items.append(item)
        item.parent = self


class Hero(Character):
    def __init__(self, game, parent):
        name = "Hero"
        description = "A brave hero trying to escape from the Ironhold prison."
        super().__init__(game, name, description, parent)
        self.inventory = Inventory(game, self)

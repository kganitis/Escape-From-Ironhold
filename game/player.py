# player.py module
from game.game_elements import Player, GameElement
from game.items import LockPick


class Inventory(GameElement):
    def __init__(self):
        name = "inventory"
        description = "Your inventory of items."
        super().__init__(name, description)
        self.items = []

    def add(self, item):
        self.items.append(item)


class Hero(Player):
    def __init__(self):
        name = "Hero"
        description = "You are a brave hero."
        super().__init__(name, description)
        self.inventory = Inventory()
        self.inventory.add(LockPick())

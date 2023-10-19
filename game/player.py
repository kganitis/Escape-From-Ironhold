# player.py module
from game.game_elements import Player
from game.items import LockPick


class Hero(Player):
    def __init__(self):
        name = "Hero"
        description = "A brave hero trying to escape from the prison."
        super().__init__(name, description)
        self.inventory.append(LockPick())

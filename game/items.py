# items.py module
from game.game_elements import Item
from game.properties import Combinable


class LockPick(Item, Combinable):
    def __init__(self, game):
        name = "lockpick"
        description = "A simple lock pick that could be useful for picking locks."
        super().__init__(game, name, description)

    def combine(self, item=None):
        if not item:
            return self.NONE_ITEM_ERROR

        if isinstance(item, Lock):
            if item.locked:
                item.locked = False
                return "lock unlocked with lockpick", self.ADVANCE_GAME_STATE
            return "lock already unlocked"
        return False


class Lock(Item, Combinable):
    def __init__(self, game, locked):
        name = "lock"
        description = "A simple lock that can could be unlocked with a lock pick, if I had one..."
        super().__init__(game, name, description)
        self.locked = locked

    def combine(self, item=None):
        if not item:
            return self.NONE_ITEM_ERROR

        if isinstance(item, LockPick):
            return item.combine(self)

        return False

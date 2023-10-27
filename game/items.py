# items.py module
from game.game_elements import Item
from game.outcomes import *
from game.properties import *


class LockPick(Item, Combinable):
    def __init__(self, game):
        name = "lockpick"
        description = "A simple lock pick that could be useful for picking locks."
        super().__init__(game, name, description)

    def combine(self, item):
        if isinstance(item, Lock):
            if item.locked:
                item.locked = False
                return LOCK_LOCKPICK_SUCCESS
            return LOCK_LOCKPICK_FAIL
        return False


class Lock(Item, Combinable):
    def __init__(self, game, locked):
        name = "lock"
        description = "A simple lock that can could be unlocked with a lock pick, if I had one..."
        super().__init__(game, name, description)
        self.locked = locked

    def combine(self, item):
        if isinstance(item, LockPick):
            return item.combine(self)
        return False

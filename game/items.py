# items.py module
from game.game_elements import Item
from game.properties import Combinable


class LockPick(Item, Combinable):
    def __init__(self):
        name = "lockpick"
        description = "A simple lock pick that could be useful for picking locks."
        super().__init__(name, description)

    def combine(self, item):
        if isinstance(item, Lock):
            lock = item
            if lock.locked:
                lock.locked = False
                outcome = "lock unlocked with lockpick"
            else:
                outcome = "lock already unlocked"
        else:
            outcome = False
        return outcome


class Lock(Item):
    def __init__(self, locked):
        name = "lock"
        description = "A simple lock that can could be unlocked with a lock pick, if I had one..."
        super().__init__(name, description)
        self.locked = locked

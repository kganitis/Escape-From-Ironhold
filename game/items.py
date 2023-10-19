# items.py module
from game.game_elements import Item


class LockPick(Item):
    def __init__(self):
        name = "lockpick"
        description = "A simple lock pick that could be useful for picking locks."
        super().__init__(name, description)
        self.chance_to_break = 0.2

    @classmethod
    def combine(cls, item):
        if isinstance(item, Lock):
            if item.locked:
                item.locked = False
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
        self.difficulty = 0.1

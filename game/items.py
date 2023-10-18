# items.py module
from game.game_elements import Item


class LockPick(Item):
    def __init__(self):
        name = "lock pick"
        description = "A simple lock pick that could be useful for picking locks."
        super().__init__(name, description)
        self.chance_to_break = 0.2

    def combine(self, item):
        if isinstance(item, Lock):
            # TODO chance to fail depending on lock difficulty
            result = item.toggle_locked()
            # TODO chance for lock pick to break
        else:
            result = False
        return result


class Lock(Item):
    def __init__(self, locked):
        name = "lock"
        description = "A simple lock that can could be unlocked with a lock pick, if I had one..."
        super().__init__(name, description)
        self.locked = locked
        self.difficulty = 0.1

    def toggle_locked(self):
        self.locked = not self.locked
        state = "locked" if self.locked else "unlocked"
        result = f"lock {state}"
        return result

from game.game_elements import LocationConnection
from game.items import Lock
from game.properties import Usable


class Door(LocationConnection, Usable):
    def __init__(self, name, description):
        super().__init__(name, description)
        self.lock = Lock(locked=True)
        self.items.append(self.lock)
        self.open = False

    def is_blocked(self):
        if self.lock.locked:
            outcome = f"The {self} is locked"
        elif not self.open:
            outcome = f"The {self} is closed"
        else:
            outcome = False
        return outcome

    def use(self):
        if self.lock.locked:
            return self.is_blocked()
        self.open = not self.open
        if self.open:
            outcome = (f"You opened the {self}", "yes")
        else:
            outcome = (f"You closed the {self}", "yes")
        return outcome

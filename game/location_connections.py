from game.game_elements import LocationConnection
from game.items import Lock
from game.outcomes import *
from game.properties import *


class Door(LocationConnection, Usable):
    def __init__(self, game, name, description):
        super().__init__(game, name, description)
        self.lock = Lock(game, locked=True)
        self.items.append(self.lock)
        self.open = False

    def is_blocked(self):
        outcome = False
        if self.lock.locked:
            outcome = DOOR_LOCKED_FAIL
        elif not self.open:
            outcome = DOOR_CLOSED_FAIL
        return outcome

    def use(self):
        if self.lock.locked:
            return self.is_blocked()

        self.open = not self.open
        if self.open:
            outcome = DOOR_OPENED_SUCCESS
        else:
            outcome = DOOR_CLOSED_SUCCESS
        return outcome

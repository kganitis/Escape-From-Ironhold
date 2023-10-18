# locations.py module
from game.items import Lock
from game_elements import Location


class Cell(Location):

    def __init__(self):
        name = "cell"
        description = "You find yourself in a dimly lit prison cell..."
        super().__init__(name, description)
        self.items.append(Lock(locked=True))

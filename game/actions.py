# actions.py module
from game.game_elements import Item, Location, LocationConnection
from game.properties import *


class Action:
    def __init__(self, command_verb, game_elements):
        # Dynamically set the action method corresponding to the command verb string
        self.execute = getattr(self, command_verb, None)
        self.game_elements = game_elements

    def is_executable(self):
        return self.execute and callable(self.execute)

    def use(self):
        two_or_more_elements = len(self.game_elements) >= 2
        if two_or_more_elements:
            return self.combine()

        object_to_use = self.game_elements[0]
        if not isinstance(object_to_use, (Item, LocationConnection)) or (not isinstance(object_to_use, (Usable, Combinable))):
            return f"Invalid object: {object_to_use}"

        outcome = object_to_use.use() if isinstance(object_to_use, Usable) else object_to_use.combine()
        return outcome or f"Can't use {object_to_use}"

    def combine(self):
        items_to_combine = self.game_elements[:2]
        invalid_items = [item for item in items_to_combine if not isinstance(item, Item)]
        if invalid_items:
            return f"Invalid item(s): {', '.join(invalid_items)}"

        item1, item2 = items_to_combine
        outcome = item1.combine(item2) or item2.combine(item1)
        return outcome or f"Can't combine {item1} and {item2}"

    def go(self):
        location_to_go = self.game_elements[0]
        if not (isinstance(location_to_go, Location) and isinstance(location_to_go, Accessible)):
            return f"Invalid location: {location_to_go}"

        outcome = location_to_go.go()
        return outcome or f"Can't go to {location_to_go}"

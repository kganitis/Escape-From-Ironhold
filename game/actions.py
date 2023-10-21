# actions.py module
from game.game_elements import Item, Location, LocationConnection
from game.properties import *


class Action:
    def __init__(self, command):
        from game.game import Game
        self.command = command
        # Convert argument stings to actual instances of game elements, retrieved from game elements repository
        self.game_elements = [Game().get_game_element(arg) for arg in command.args]

    def execute(self):
        # Dynamically get the action method corresponding to the command verb string
        verb = self.command.verb.lower()
        action = getattr(self, verb, None)
        if action and callable(action):
            outcome = action()
            return outcome
        else:
            raise ValueError(f"Action not found for verb: {verb}")

    def use(self):
        two_or_more_elements = len(self.game_elements) >= 2
        if two_or_more_elements:
            return self.combine()

        object_to_use = self.game_elements[0]
        if not (isinstance(object_to_use, Item) or isinstance(object_to_use, LocationConnection)):
            return f"Invalid object: {object_to_use}"

        outcome = False
        if isinstance(object_to_use, Usable):
            outcome = object_to_use.use()
        if not outcome:
            outcome = f"Can't use {object_to_use}"
        return outcome

    def combine(self):
        items_to_combine = self.game_elements
        item1 = items_to_combine[0]
        item2 = items_to_combine[1]

        invalid_items = [f"{item}" for item in items_to_combine if not isinstance(item, Item)]
        if invalid_items:
            return f"Invalid item(s): {', '.join(invalid_items)}"

        outcome = False
        if isinstance(item1, Combinable):
            outcome = item1.combine(item2)
        elif isinstance(item2, Combinable):
            outcome = item2.combine(item1)
        if not outcome:
            outcome = f"Can't combine {item1} and {item2}"
        return outcome

    def go(self):
        location_to_go = self.game_elements[0]
        if not isinstance(location_to_go, Location):
            return f"Invalid location: {location_to_go}"

        outcome = False
        if isinstance(location_to_go, Accessible):
            outcome = location_to_go.go()
        if not outcome:
            outcome = f"Can't go to {location_to_go}"
        return outcome

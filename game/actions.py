# actions.py module
from game.game_elements import game_elements_repository, Item


class Action:
    def __init__(self, command):
        self.command = command
        # Convert argument stings to actual instances of game elements, retrieved from game elements repository
        self.elements = [game_elements_repository.get(arg, arg) for arg in command.args]

    def execute(self):
        # Dynamically get the action method corresponding to the command verb string
        action = getattr(self, self.command.verb.lower(), None)
        if action and callable(action):
            outcome = action()
            return outcome
        else:
            raise ValueError(f"Action not found for verb: {self.command.verb}")

    def use(self):
        if len(self.elements) >= 2:  # if two or more items, execute combine instead
            return self.combine()

        item = self.elements[0]  # the item to be used
        if not isinstance(item, Item):  # check if it's a valid item
            return f"Invalid item: {item}"

        outcome = False
        # check if the item has a 'use' method
        if hasattr(item, 'use') and callable(getattr(item, 'use')):
            outcome = item.use()

        if not outcome:
            outcome = f"can't use {item}"

        return outcome

    def combine(self):
        items = self.elements  # the items to be combined

        # check if items list contains invalid game items
        invalid_items = [item for item in items if not isinstance(item, Item)]
        if invalid_items:
            return f"Invalid item(s): {', '.join(invalid_items)}"

        outcome = False
        # Check if at least one of the items has a 'combine' method
        if hasattr(items[0], 'combine') and callable(getattr(items[0], 'combine')):
            outcome = items[0].combine(items[1])
        elif hasattr(items[1], 'combine') and callable(getattr(items[1], 'combine')):
            outcome = items[1].combine(items[0])

        if not outcome:
            outcome = f"can't combine {items[0]} and {items[1]}"

        return outcome


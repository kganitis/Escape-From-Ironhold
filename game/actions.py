# actions.py module
from game.game_elements import game_elements_repository


class Action:
    def __init__(self, command):
        self.command = command
        # Convert arg stings to actual instances of game elements, retrieved from game elements repository
        self.elements = [game_elements_repository[arg] for arg in command.args]

    def execute(self):
        action = self.action()
        outcome = action()
        return outcome

    def action(self):
        # Dynamically get the action method corresponding to the command verb string
        action = getattr(self, self.command.verb.lower(), None)
        if action and callable(action):
            return action
        else:
            raise ValueError(f"Action not found for verb: {self.command.verb}")

    def use(self):
        if len(self.elements) >= 2:  # if two or more items, execute combine instead
            return self.combine()
        item = self.elements[0]  # the item to be used
        outcome = item.use()
        if not outcome:
            outcome = f"can't use {item}"
        return outcome

    # TODO check if items list contains valid game items
    def combine(self):
        items = self.elements  # the items to be combined
        outcome = items[0].combine(items[1]) or items[1].combine(items[0])
        if not outcome:
            outcome = f"can't combine {items[0]} and {items[1]}"
        return outcome

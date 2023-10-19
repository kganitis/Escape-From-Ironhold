# actions.py module
from game.game_elements import get_game_element, Action


class Use(Action):
    def __init__(self, items):
        name = "use"
        description = "Use an item"
        super().__init__(name, description)
        self.item = items  # the item to be used

    def execute(self):
        if isinstance(self.item, list):  # if two or more items, execute combine instead
            action = Combine(self.item)
            return action.execute()
        else:
            pass


class Combine(Action):
    def __init__(self, items):
        name = "combine"
        description = "Combine multiple items"
        super().__init__(name, description)

        if not isinstance(items, list):
            raise ValueError("Items must be provided as a list.")
        self.items = items  # the items to be combined

        # convert item name strings to item instances found in game elements repository
        self.items = [get_game_element(item) for item in items]

        # TODO check if items list contains valid game items

    def execute(self):
        outcome = self.items[0].combine(self.items[1])
        if not outcome:
            outcome = f"can't combine {self.items[0]} and {self.items[1]}"
        return outcome


class Go(Action):
    def __init__(self, another_location=None):
        name = "go"
        description = "Go to another location"
        super().__init__(name, description)
        self.new_location = another_location

    def execute(self):
        pass

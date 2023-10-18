# actions.py module
from game.game_elements import get_game_element, Action


class Use(Action):
    def __init__(self, items):
        name = "use"
        description = "Use an item"
        super().__init__(name, description)
        if isinstance(items, list):  # if two or more items, execute combine instead
            action = Combine(items)
            action.execute()
        else:
            self.item = items  # the item to be used

    def attempt(self):
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

    def attempt(self):
        self.result = self.items[0].combine(self.items[1])
        if not self.result:
            self.result = f"can't combine {self.items[0]} and {self.items[1]}"


class Go(Action):
    def __init__(self, another_location=None):
        name = "go"
        description = "Go to another location"
        super().__init__(name, description)
        self.new_location = another_location

    def attempt(self):
        pass

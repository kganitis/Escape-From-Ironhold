# actions.py module
from game.game_elements import get_game_element
from game_elements import Action


class Use(Action):
    def __init__(self, items):
        name = "use"
        description = "Use an item"
        super().__init__(name, description)
        if isinstance(items, list):
            pass  # combine items instead
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

        # TODO check if items list contains valid game items
        items = [get_game_element(item) for item in items]

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

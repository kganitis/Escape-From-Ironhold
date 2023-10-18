from game.game_elements import Player


class Hero(Player):
    def __init__(self):
        name = "Hero"
        description = "A brave hero trying to escape from the prison."
        super().__init__(name, description)

    def add_item_to_inventory(self, item):
        self.inventory.append(item)

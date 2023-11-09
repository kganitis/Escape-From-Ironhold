from .world import World


class Game:
    def __init__(self, test=False):
        self.test = test
        self.world = World()
        self.world.populate()

    def run(self):
        while True:
            print("\nWhat do you want to do?")
            input_command = input("> ")
            self.world.parse(input_command)

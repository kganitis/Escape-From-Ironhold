# game.py module
from chatbot.chatbot import *
from .world import World


class Game:
    def __init__(self, test=False):
        self.test = test
        self.world = World()

    def run(self):
        self.world.populate()
        print("Escape From Ironhold: Prison Cell")
        self.current_location.describe()
        while True:
            print("\nWhat do you want to do? (type 'help' for commands)")
            input_command = input("> ").strip().lower()
            # TODO send command input string to nlp package for parsing
            results = parse(self.world, input_command)
            if not self.test:
                for result in results:
                    print(f"\n{result.outcome} {result.related_objects}")

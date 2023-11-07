from .world import World
from nlp.parser import parse


class Game:
    def __init__(self, test=False):
        self.test = test
        self.world = World()

    def run(self):
        self.world.populate()
        print("Escape From Ironhold: Prison Cell")
        while True:
            print("\nWhat do you want to do?")
            input_command = input("> ").strip().lower()
            results = parse(self.world, input_command)
            if not self.test:
                for result in results:
                    print(f"\n{result.outcome} {result.related_objects}")

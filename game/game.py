# game.py module
from chatbot.chatbot import *
from .world import World
from .commands import Command
from .actions import Action
from .outcomes import INVALID_COMMAND
from .result import Result


class Game:
    def __init__(self, test=False):
        self.test = test

        # A repository to hold every game object created
        # It maps the object's name to the actual instance of the game object
        self.game_objects_repository = {}

        # Initialize game objects here
        self.game_world = World(self)

    @property
    def current_location(self):
        return self.game_world.current_location

    @property
    def player(self):
        return self.game_world.hero

    def run(self):
        self.game_world.populate()
        print("Escape From Ironhold: Prison Cell")
        self.current_location.describe()
        while True:
            print("\nWhat do you want to do? (type 'help' for commands)")
            input_command = input("> ").strip().lower()
            # TODO send command input string to nlp package for parsing
            self.parse(input_command)

    def parse(self, input_command):
        # Split the command into words
        words = input_command.split()
        verb = words[0]  # The first word is the verb
        args = words[1:] if len(words) > 1 else None  # The rest of the words, if more exist, are arguments

        # Create the command and check syntax
        command = Command(verb, args)
        if command.is_valid():
            # Map argument stings to actual instances of game objects, retrieved from the game objects repository
            game_objects = [self.game_objects_repository.get(arg, arg) for arg in command.args]
            # Execute the command
            action = Action(self, command, game_objects)
            results = action.execute()
        else:
            outcome_text, outcome_type = INVALID_COMMAND
            results = [Result(command, outcome_text, [], outcome_type)]

        # Print the results
        if self.test:
            return results
        for result in results:
            print(f"\n{result.outcome} {result.related_objects}")
            # message = generate_message(result)
            # print(f"Message: {message}")

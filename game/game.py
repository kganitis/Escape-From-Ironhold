# game.py module
from chatbot.chatbot import *
from .locations import Cell
from .character import Hero
from .commands import Command, show_available_commands
from .actions import Action
from .outcomes import *
from .result import Result


class Game:
    def __init__(self, test=False):
        self.test = test

        # A repository to hold every game element created
        # It maps the element's name to the actual instance of the game element
        self.game_elements_repository = {}

        self.result_history = []

        # Initialize game elements here
        self.current_location = Cell(self)
        self.player = Hero(self, self.current_location)

    def run(self):
        print("Escape From Ironhold: Prison Cell")
        self.current_location.describe()
        while True:
            print("\nWhat do you want to do? (type 'help' for commands)")
            input_command = input("> ").strip().lower()

            # TODO send command input string to nlp package for parsing

            # further parse the command to translate it into an in game action
            if input_command == "help":
                show_available_commands()
                continue
            elif input_command == "exit":
                print("Goodbye!")
                break
            elif input_command == '':
                print("Empty input!")
                continue
            else:
                self.parse(input_command)

    def parse(self, input_command):
        # Split the command into words
        words = input_command.split()
        if not words:
            return None
        verb = words[0]  # The first word is the verb
        args = words[1:] if len(words) > 1 else None  # The rest of the words, if more exist, are arguments

        # Execute the command
        command = Command(verb, args)
        outcome_text, outcome_type = INVALID_COMMAND
        results = [Result(command, outcome_text, [], outcome_type)]
        if command.is_valid():
            # Convert argument stings to actual instances of game elements, retrieved from the game elements repository
            game_elements = [self.game_elements_repository.get(arg, arg) for arg in command.args]
            action = Action(self, command, game_elements)
            if action.is_executable():
                action.execute()
                results = action.results
            else:
                raise ValueError(f"Action not found for verb: {command.verb}")
        self.result_history.extend(results)

        if self.test:
            return results
        for result in results:
            print(f"\n{result.outcome} {result.related_elements}")
            # message = generate_message(result)
            # print(f"Message: {message}")

from game.actions import Action
from game.commands import *
from game.outcomes import Outcome, INVALID_COMMAND
from game.result import Result


stop_words = ['the', 'a', 'an', 'and', 'in', 'on', 'to', 'with', 'for', 'as', 'at', 'from']


def parse(world, input_command, test=False):
    # Tokenizing
    words = [word for word in input_command.strip().lower().split() if word not in stop_words]
    # Extract the first word as the verb
    verb = words[0]
    nouns = words[1:] if len(words) > 1 else None

    command = Command(verb, nouns)

    # Check if asked for help
    if command.verb == 'help':
        show_help(command.nouns)
        return

    # Lexical Analysis
    game_objects = [world.get(noun) for noun in command.nouns]
    primary_object = game_objects[0] if game_objects else None
    secondary_object = game_objects[1] if len(game_objects) > 1 else None

    # Syntax Analysis
    if not command.is_valid():
        action = Action(world, command)
        outcome = Outcome(INVALID_COMMAND)
        result = Result(action, outcome)
    else:
        # Execution
        action = Action(world, command, primary_object, secondary_object)
        outcome = action.execute()
        result = Result(action, outcome)

    # Print
    if not test:
        result.show()
    return result


def show_help(command=None):
    verb = command[0] if command and command[0] in get_available_command_verbs() else None
    examples = 'examples' if verb and len(command) == 2 and command[1] == 'examples' else None

    if examples:
        show_examples_for_verb(verb)
    elif verb:
        show_syntax_for_verb(verb)
        print("Type 'help {command} examples' to get examples for a specific command.")
    else:
        show_available_commands()
        print("Type 'help {command}' to get help for a specific command.")

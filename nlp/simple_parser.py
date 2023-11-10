from game.actions import Action
from game.commands import Command
from game.outcomes import Outcome, INVALID_COMMAND
from game.result import Result


stop_words = ["the", "a", "an", "and", "in", "on", "to", "with", "for", "as", "at", "from"]


def parse(world, input_command, test=False):
    # Tokenizing
    words = [word for word in input_command.strip().lower().split() if word not in stop_words]
    # Extract the first word as the verb
    verb = words[0]
    words = words[1:] if len(words) > 1 else None

    command = Command(verb, words)

    # Lexical Analysis
    game_objects = [world.game_objects_repository.get(word, word) for word in command.words]
    primary_object = game_objects[0] if len(game_objects) > 0 else None
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

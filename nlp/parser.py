from game.actions import Action
from game.commands import Command
from game.outcomes import INVALID_COMMAND
from game.result import Result


def parse(world, input_command):
    # Tokenizing
    words = input_command.split()
    verb = words[0]  # The first word is the verb
    args = words[1:] if len(words) > 1 else None  # The rest of the words, if more exist, are arguments

    # Syntax Analysis
    command = Command(verb, args)
    if not command.is_valid():
        outcome_text, outcome_type = INVALID_COMMAND
        return [Result(command, outcome_text, [], outcome_type)]

    # Lexical Analysis
    game_objects = [world.game_objects_repository.get(arg, arg) for arg in command.args]
    direct_object = game_objects[0] if len(game_objects) > 0 else None
    indirect_object = game_objects[1] if len(game_objects) > 1 else None

    # Execution
    action = Action(world, command, direct_object, indirect_object)
    return action.execute()
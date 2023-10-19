# command.py module
from game.actions import *
from game.result import Result


# Quantifier functions
# Check if an arguments list contains certain element count
# Used to ensure that a command is followed by a valid count of arguments
def __args_count_is_at_most(args, quantity):  # useful to represent the '?' quantifier, meaning 0 or 1
    return len(args) <= quantity


def __args_count_is_at_least(args, quantity):  # useful to represent the '+' quantifier, meaning 1 or more
    return len(args) >= quantity


def __args_count_is_exactly(args, quantity):  # useful to check if a command must be followed by exactly 0 or 1 argument
    return len(args) == quantity


# Define rules for the required number of arguments for each command.
# The key is the command's verb, and the value is a rule (quantifier, quantity).
# The quantifier checks if the argument count follows the quantity limitation.
# For instance, the "look" command allows at most 1 argument.
_command_structure_rules = {
    "look": (__args_count_is_at_most, 1),
    "go": (__args_count_is_exactly, 1),
    "examine": (__args_count_is_at_most, 1),
    "take": (__args_count_is_exactly, 1),
    "use": (__args_count_is_at_least, 1),
    "combine": (__args_count_is_at_least, 2),
    "fight": (__args_count_is_exactly, 1),
    "wait": (__args_count_is_exactly, 0),
    "help": (__args_count_is_exactly, 0),
    "exit": (__args_count_is_exactly, 0)
}


def get_available_command_verbs():
    return _command_structure_rules.keys()


def _get_quantifier_function(verb):
    return _command_structure_rules[verb][0]


def _get_args_count_limitation(verb):
    return _command_structure_rules[verb][1]


class Command:
    def __init__(self, verb, args=None):
        self.verb = verb
        if args is None:
            args = []
        self.args = args
        self.result = Result(command=f"{self}")

    def __str__(self):
        return f"{self.verb} {' '.join(self.args)}"

    def __is_valid_verb(self):
        valid_verbs = get_available_command_verbs()
        is_valid_verb = self.verb in valid_verbs
        return is_valid_verb

    def __args_count_is_valid(self):
        quantifier = _get_quantifier_function(self.verb)
        quantity = _get_args_count_limitation(self.verb)
        args_count_is_valid = quantifier(self.args, quantity)
        return args_count_is_valid

    def __is_valid(self):
        return self.__is_valid_verb() and self.__args_count_is_valid()

    def execute(self):
        if self.__is_valid():
            # Dynamically create an instance of the action class corresponding to the verb
            action_class = globals().get(self.verb.capitalize())
            if action_class:
                action = action_class(self.args)
                outcome = action.execute()
            else:
                outcome = f"Action not found: {self}"
        else:
            outcome = f"Invalid command: {self}"
        self.result.outcome = outcome
        return self.result

# command.py module

# Quantifier functions
# Check if an arguments list contains certain arguments count
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
_available_commands = {
    "go": {
        "rule": (__args_count_is_exactly, 1),
        "description": "Go to a specific location or in a particular direction.",
        "syntax": "go {direction}|{location}"
    },
    "examine": {
        "rule": (__args_count_is_at_most, 1),
        "description": "Examine an item or the current location.",
        "syntax": "examine {item}?|{location}?"
    },
    "take": {
        "rule": (__args_count_is_exactly, 1),
        "description": "Take a specific item.",
        "syntax": "take {item}"
    },
    "use": {
        "rule": (__args_count_is_at_least, 1),
        "description": "Use an object or perform an action using one or more objects.",
        "syntax": "use {item}+|{location_connection}+"
    },
    "combine": {
        # it's allowed to follow combine with only one item, but will always lead to an error message from the narrator
        "rule": (__args_count_is_at_least, 1),
        "description": "Combine two or more items.",
        "syntax": "combine {item}+"
    },
    "talk": {
        "rule": (__args_count_is_exactly, 1),
        "description": "Talk to a character.",
        "syntax": "fight {character}"
    },
    "fight": {
        "rule": (__args_count_is_exactly, 1),
        "description": "Engage in a fight with a character.",
        "syntax": "fight {character}"
    },
    "wait": {
        "rule": (__args_count_is_exactly, 0),
        "description": "Wait for some hours.",
        "syntax": "wait"
    },
    "inventory": {
        "rule": (__args_count_is_exactly, 0),
        "description": "Show player's inventory of items.",
        "syntax": "inventory"
    },
    "help": {
        "rule": (__args_count_is_exactly, 0),
        "description": "Get assistance or see available commands.",
        "syntax": "help {command}?"
    },
    "exit": {
        "rule": (__args_count_is_exactly, 0),
        "description": "Exit the game.",
        "syntax": "help"
    }
}


def get_available_command_verbs():
    available_command_verbs = _available_commands.keys()
    available_command_verbs = ["use", "combine", "go"]  # TODO delete this once all commands have been implemented
    return available_command_verbs


def _get_quantifier_function(verb):
    return _available_commands[verb]["rule"][0]


def _get_args_count_limitation(verb):
    return _available_commands[verb]["rule"][1]


class Command:
    def __init__(self, verb, args=None):
        from game.result import Result
        self.verb = verb
        # Make sure args is a list
        if args is None:
            args = []
        if not isinstance(args, list):
            args = [arg for arg in args]
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
            from game.actions import Action
            outcome = Action(self).execute()
        else:
            outcome = f"Invalid command: {self}"
        if isinstance(outcome, tuple):
            self.result.outcome = outcome[0]
            self.result.advance = outcome[1]
        else:
            self.result.outcome = outcome
        return self.result

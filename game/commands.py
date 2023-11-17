# Quantifier functions
# Used to ensure that a command is followed by a certain count of nouns
def noun_count_is_at_most(nouns, quantity):
    return len(nouns) <= quantity


def noun_count_is_at_least(nouns, quantity):
    return len(nouns) >= quantity


def noun_count_is_not_zero_and_at_most(nouns, quantity):
    return len(nouns) > 0 and len(nouns) <= quantity


def noun_count_is_exactly(nouns, quantity):
    return len(nouns) == quantity


# Define rules for the required number of arguments for each command.
# The key is the command's verb, and the value is a rule (quantifier, quantity).
# The quantifier checks if the word count follows the quantity limitation.
# For example, the "examine" command must be followed by 1 word at most.
_available_commands = {
    'go': {
        'rule': (noun_count_is_exactly, 1),
        'description': "Go to the specified room.",
        'syntax': "go to the {room}",
        'examples': ["Go to the dungeon"],
        'synonyms': ['access', 'enter']
    },
    'exit': {
        'rule': (noun_count_is_at_most, 2),
        'description': "Exit (the current room) (from a specified exit).",
        'syntax': "exit (the {room}) (from the {connection})",
        'examples': ["Exit", "Exit the cell", "Exit the dungeon from the window", "Exit from the window"]
    },
    'examine': {
        'rule': (noun_count_is_at_most, 1),
        'description': "Examine the current room (or an object).",
        'syntax': "examine (the {object}?|{room})",
        'examples': ["Examine", "Examine the cell", "Examine the door"],
        'synonyms': ['search', 'look', 'inspect']
    },
    'take': {
        'rule': (noun_count_is_not_zero_and_at_most, 2),
        'description': "Take the specified item.",
        'syntax': "take the {item} (from the {object})",
        'examples': ["Take the lockpick"],
        'synonyms': ['steal', 'grab', 'acquire', 'pick']
    },
    'drop': {
        'rule': (noun_count_is_exactly, 1),
        'description': "Drop the specified item.",
        'syntax': "drop the {item}",
        'examples': ["Drop the lockpick"]
    },
    'use': {
        'rule': (noun_count_is_not_zero_and_at_most, 2),
        'description': "Use an object (with/on another object).",
        'syntax': "use the {object} (on/with the {object})",
        'examples': ["Use the lockpick", "Use the lockpick on the lock"]
    },
    'lock': {
        'rule': (noun_count_is_not_zero_and_at_most, 2),
        'description': "Lock a lockable object (with a specified item).",
        'syntax': "lock the {object} (with the {item})",
        'examples': ["Lock the door", "Lock the door with the key"]
    },
    'unlock': {
        'rule': (noun_count_is_not_zero_and_at_most, 2),
        'description': "Unlock an unlockable object (with a specified item).",
        'syntax': "unlock the {object} (with the {item})",
        'examples': ["Unlock the lock", "Unlock the lock with the lockpick"],
        'synonyms': ['pick']
    },
    'open': {
        'rule': (noun_count_is_not_zero_and_at_most, 2),
        'description': "Open an object (with a specified item).",
        'syntax': "open the {object} (with the {item})",
        'examples': ["Open the door", "Open the door with the lockpick"]
    },
    'close': {
        'rule': (noun_count_is_exactly, 1),
        'description': "Close an object.",
        'syntax': "close the {object}",
        'examples': ["Close the door"],
        'synonyms': ['shut']
    },
    'wake': {
        'rule': (noun_count_is_exactly, 1),
        'description': "Wake up an animate.",
        'syntax': "wake (up) the {object}",
        'examples': ["Wake up the guard"],
        'synonyms': ['awaken']
    },
    'attack': {
        'rule': (noun_count_is_not_zero_and_at_most, 2),
        'description': "Attack another animate (with an object).",
        'syntax': "attack the {animate} (with the {object}.",
        'examples': ["Attack the guard with the lockpick"],
        'synonyms': ['fight', 'assault', 'confront']
    },
    'ask': {
        'rule': (noun_count_is_at_least, 1),
        'description': "Ask an animate something.",
        'syntax': "ask the {animate} {any}",
        'examples': ["Ask the guard why I'm here."]
    },
    'tell': {
        'rule': (noun_count_is_at_least, 1),
        'description': "Tell an animate something",
        'syntax': "tell the {animate} {any}",
        'examples': ["Tell the guard to set me free."],
        'synonyms': ['demand', 'order']
    },
    'throw': {
        'rule': (noun_count_is_not_zero_and_at_most, 2),
        'description': "Throw an {object} (at another {object})",
        'syntax': "throw the {object} (at the {object})",
        'examples': ["Throw the lockpick", "Throw the stone at the guard"],
        'synonyms': ['shoot', 'launch']
    },
    # TODO implement sneak, walk, approach and run in some way
    # TODO implement try
    # '': {
    #     'rule': (),
    #     'description': "",
    #     'syntax': "",
    #     'examples': [],
    #     'synonyms': []
    # },
    'wait': {
        'rule': (noun_count_is_at_least, 0),
        'description': "Do nothing this turn.",
        'syntax': "wait",
        'examples': ["Wait"]
    },
    # 'inventory': {
    #     'rule': (words_count_is_exactly, 0),
    #     'description': "Show player's inventory of items.",
    #     'syntax': "inventory"
    # },
    'help': {
        'rule': (noun_count_is_at_most, 2),
        'description': "See available commands or get help for a specific command.",
        'syntax': "help {command}? {examples}?",
        'examples': ["Help", "Help take", "Help take examples"]
    }
}


def get_available_command_verbs():
    available_command_verbs = list(_available_commands.keys())
    return available_command_verbs


def show_available_commands():
    print("Available commands:")
    print(", ".join([command for command in get_available_command_verbs()]))


def show_syntax_for_verb(verb):
    print(f"Syntax for {verb}:")
    print(_available_commands[verb]['syntax'])


def show_examples_for_verb(verb):
    print(f"Examples for {verb}:")
    print(", ".join([example for example in _available_commands[verb]['examples']]))


def synonym_of(verb):
    for key, value in _available_commands.items():
        if 'synonyms' in value and verb in value['synonyms']:
            return key
    return None


stop_words = ['the', 'a', 'an', 'and', 'in', 'on', 'to', 'with', 'for', 'as', 'at', 'from', 'up']


class Command:
    def __init__(self, verb, words=None):
        self.verb = verb
        self.__original_verb = verb
        self.__synonym = None
        if verb not in get_available_command_verbs():
            self.__synonym = synonym_of(verb)
            self.verb = self.__synonym or self.verb

        # Make sure words is a list
        if words is None:
            words = []
        if not isinstance(words, list):
            words = [word for word in words]
        self.nouns = [word for word in words if word not in stop_words]

    def __str__(self):
        return f"{self.__original_verb} {' '.join(self.nouns)}"

    def is_valid(self):
        if self.verb in ('ask', 'tell'):
            return True

        if not self.__synonym and self.__original_verb not in get_available_command_verbs():
            return False

        quantifier_function, noun_limit = _available_commands[self.verb]['rule']
        if not quantifier_function(self.nouns, noun_limit):
            return False

        return True

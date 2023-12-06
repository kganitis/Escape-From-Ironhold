from game_object import GameObject
from lexicon import prepositions as preposition


syntax_rules = {
    'take': [
        {
            'tokens': [GameObject],
            'action': 'take',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [GameObject, ['from', 'off', 'away', 'out'], GameObject],
            'action': 'take',
            'primary': 0,
            'secondary': 2
        },
        {
            'tokens': [GameObject, ['off', 'out'], ['from', 'off'], GameObject],
            'action': 'take',
            'primary': 0,
            'secondary': 3
        }
    ],
    'get': [
        {
            'tokens': [GameObject],
            'action': 'take',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [GameObject, 'from', GameObject],
            'action': 'take',
            'primary': 0,
            'secondary': 2
        },
        {
            'tokens': [GameObject, ['off', 'out'], ['from', 'of'], GameObject],
            'action': 'take',
            'primary': 0,
            'secondary': 3
        }
    ],
    'pick': [
        {
            'tokens': [GameObject],
            'action': 'unlock',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [GameObject, ['with', 'using'], GameObject],
            'action': 'unlock',
            'primary': 0,
            'secondary': 2
        },
        {
            'tokens': ['up', GameObject],
            'action': 'take',
            'primary': 1,
            'secondary': None
        },
        {
            'tokens': ['up', GameObject, 'from', GameObject],
            'action': 'take',
            'primary': 1,
            'secondary': 3
        },
        {
            'tokens': ['up', GameObject, ['off', 'out'], ['from', 'of'], GameObject],
            'action': 'take',
            'primary': 1,
            'secondary': 4
        }
    ],
    'use': [
        {
            'tokens': [GameObject],
            'action': 'use',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [GameObject, preposition, GameObject],
            'action': 'use',
            'primary': 0,
            'secondary': 2
        },
    ],
    '': [
        {
            'tokens': [],
            'action': '',
            'primary': 0,
            'secondary': 0
        },
    ],
}

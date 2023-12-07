from game_object import GameObject
from lexicon import prepositions as preposition


syntax_rules = {
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
        },
        {
            'tokens': [['to', 'in', 'into', 'at'], GameObject],
            'action': 'go',
            'primary': 1,
            'secondary': None
        },
        {
            'tokens': [['to', 'in', 'into', 'at'], GameObject, ['from', 'through', 'by', 'using'], GameObject],
            'action': 'go',
            'primary': 1,
            'secondary': 3
        },
        {
            'tokens': [['from', 'through', 'by', 'using'], GameObject, ['to', 'in', 'into', 'at'], GameObject],
            'action': 'go',
            'primary': 3,
            'secondary': 1
        },
        {
            'tokens': [['through'], GameObject],
            'action': 'exit',
            'primary': 1,
            'secondary': None
        },
        {
            'tokens': ['out', 'of', GameObject],
            'action': 'exit',
            'primary': 2,
            'secondary': None
        },
        {
            'tokens': ['out', 'of', GameObject, ['from', 'through', 'by', 'using'], GameObject],
            'action': 'exit',
            'primary': 2,
            'secondary': 4
        }
    ],
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
    'drop': [
        {
            'tokens': [GameObject],
            'action': 'drop',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [GameObject, GameObject],
            'action': 'drop',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [GameObject, preposition, GameObject],
            'action': 'drop',
            'primary': 0,
            'secondary': None
        },
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
        }
    ],
    'go': [
        {
            'tokens': [GameObject],
            'action': 'go',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [['to', 'in', 'into', 'at'], GameObject],
            'action': 'go',
            'primary': 1,
            'secondary': None
        },
        {
            'tokens': [GameObject, ['from', 'through', 'by', 'using'], GameObject],
            'action': 'go',
            'primary': 0,
            'secondary': 2
        },
        {
            'tokens': [['to', 'in', 'into', 'at'], GameObject, ['from', 'through', 'by', 'using'], GameObject],
            'action': 'go',
            'primary': 1,
            'secondary': 3
        },
        {
            'tokens': [['from', 'through', 'by', 'using'], GameObject, ['to', 'in', 'into', 'at'], GameObject],
            'action': 'go',
            'primary': 3,
            'secondary': 1
        },
        {
            'tokens': [['from', 'through', 'by', 'using'], GameObject],
            'action': 'exit',
            'primary': 1,
            'secondary': None
        },
        {
            'tokens': ['out', 'of', GameObject],
            'action': 'exit',
            'primary': 2,
            'secondary': None
        },
        {
            'tokens': ['out', 'of', GameObject, ['from', 'through', 'by', 'using'], GameObject],
            'action': 'exit',
            'primary': 2,
            'secondary': 4
        }
    ],
    'enter': [
        {
            'tokens': [GameObject],
            'action': 'enter',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [['to', 'in', 'into', 'at'], GameObject],
            'action': 'enter',
            'primary': 1,
            'secondary': None
        },
        {
            'tokens': [GameObject, ['from', 'through', 'by', 'using'], GameObject],
            'action': 'go',
            'primary': 0,
            'secondary': 2
        },
        {
            'tokens': [['to', 'in', 'into', 'at'], GameObject, ['from', 'through', 'by', 'using'], GameObject],
            'action': 'go',
            'primary': 1,
            'secondary': 3
        },
        {
            'tokens': [['from', 'through', 'by', 'using'], GameObject, ['to', 'in', 'into', 'at'], GameObject],
            'action': 'go',
            'primary': 3,
            'secondary': 1
        },
        {
            'tokens': [['from', 'through', 'by', 'using'], GameObject],
            'action': 'exit',
            'primary': 1,
            'secondary': None
        }
    ],
    'exit': [
        {
            'tokens': [GameObject],
            'action': 'exit',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [['to', 'in', 'into', 'at'], GameObject],
            'action': 'go',
            'primary': 1,
            'secondary': None
        },
        {
            'tokens': [GameObject, ['from', 'through', 'by', 'using'], GameObject],
            'action': 'exit',
            'primary': 0,
            'secondary': 2
        },
        {
            'tokens': [['to', 'in', 'into', 'at'], GameObject, ['from', 'through', 'by', 'using'], GameObject],
            'action': 'go',
            'primary': 1,
            'secondary': 3
        },
        {
            'tokens': [['from', 'through', 'by', 'using'], GameObject, ['to', 'in', 'into', 'at'], GameObject],
            'action': 'go',
            'primary': 3,
            'secondary': 1
        },
        {
            'tokens': [['from', 'through', 'by', 'using'], GameObject],
            'action': 'exit',
            'primary': 1,
            'secondary': None
        }
    ],
    'leave': [
        {
            'tokens': [GameObject],
            'action': 'leave',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [['to', 'in', 'into', 'at'], GameObject],
            'action': 'go',
            'primary': 1,
            'secondary': None
        },
        {
            'tokens': [GameObject, ['from', 'through', 'by', 'using'], GameObject],
            'action': 'exit',
            'primary': 0,
            'secondary': 2
        },
        {
            'tokens': [GameObject, ['in', 'at', 'on', 'to', 'into', 'onto'], GameObject],
            'action': 'drop',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [['to', 'in', 'into', 'at'], GameObject, ['from', 'through', 'by', 'using'], GameObject],
            'action': 'go',
            'primary': 1,
            'secondary': 3
        },
        {
            'tokens': [['from', 'through', 'by', 'using'], GameObject, ['to', 'in', 'into', 'at'], GameObject],
            'action': 'go',
            'primary': 3,
            'secondary': 1
        },
        {
            'tokens': [['from', 'through', 'by', 'using'], GameObject],
            'action': 'exit',
            'primary': 1,
            'secondary': None
        }
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

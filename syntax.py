from game_object import GameObject
from lexicon import prepositions as preposition


held = []

syntax_rules = {
    'get': [
        {
            'tokens': [GameObject],
            'action': 'take',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [GameObject, ['from'], GameObject],
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
            'tokens': [['out'], ['of'], GameObject],
            'action': 'exit',
            'primary': 2,
            'secondary': None
        },
        {
            'tokens': [['out'], ['of'], GameObject, ['from', 'through', 'by', 'using'], GameObject],
            'action': 'exit',
            'primary': 2,
            'secondary': 4
        },
        {
            'tokens': [['rid'], ['of'], held],
            'action': 'drop',
            'primary': 2,
            'secondary': None
        },
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
            'tokens': [GameObject, ['off', 'out'], ['from', 'off', 'of'], GameObject],
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
            'tokens': [['up'], GameObject],
            'action': 'take',
            'primary': 1,
            'secondary': None
        },
        {
            'tokens': [GameObject, ['up']],
            'action': 'take',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [['up'], GameObject, ['from'], GameObject],
            'action': 'take',
            'primary': 1,
            'secondary': 3
        },
        {
            'tokens': [['up'], GameObject, ['off', 'out'], ['from', 'of'], GameObject],
            'action': 'take',
            'primary': 1,
            'secondary': 4
        }
    ],
    'drop': [
        {
            'tokens': [held],
            'action': 'drop',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [held, preposition, GameObject],
            'action': 'drop',
            'primary': 0,
            'secondary': None
        },
    ],
    'use': [
        {
            'tokens': [held],
            'action': 'use',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [held, preposition, GameObject],
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
            'tokens': [['out'], ['of'], GameObject],
            'action': 'exit',
            'primary': 2,
            'secondary': None
        },
        {
            'tokens': [['out'], ['of'], GameObject, ['from', 'through', 'by', 'using'], GameObject],
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
            'tokens': [held, ['in', 'at', 'on', 'to', 'into', 'onto'], GameObject],
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
    'examine': [
        {
            'tokens': [],
            'action': 'examine',
            'primary': None,
            'secondary': None
        },
        {
            'tokens': [GameObject],
            'action': 'examine',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [preposition, GameObject],
            'action': 'examine',
            'primary': 1,
            'secondary': None
        },
        {
            'tokens': [preposition],
            'action': 'examine',
            'primary': None,
            'secondary': None
        },
    ],
    'lock': [
        {
            'tokens': [GameObject],
            'action': 'lock',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [GameObject, ['with', 'using'], held],
            'action': 'lock',
            'primary': 0,
            'secondary': 2
        },
    ],
    'unlock': [
        {
            'tokens': [GameObject],
            'action': 'unlock',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [GameObject, ['with', 'using'], held],
            'action': 'unlock',
            'primary': 0,
            'secondary': 2
        },
    ],
    'open': [
        {
            'tokens': [GameObject],
            'action': 'open',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [GameObject, ['with', 'using'], held],
            'action': 'open',
            'primary': 0,
            'secondary': 2
        },
    ],
    'close': [
        {
            'tokens': [GameObject],
            'action': 'close',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [GameObject, ['with', 'using'], GameObject],
            'action': 'close',
            'primary': 0,
            'secondary': 2
        },
    ],
    'wake': [
        {
            'tokens': [GameObject],
            'action': 'wake',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [GameObject, ['up']],
            'action': 'wake',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [['up'], GameObject],
            'action': 'wake',
            'primary': 1,
            'secondary': None
        },
    ],
    'attack': [
        {
            'tokens': [GameObject],
            'action': 'attack',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [GameObject, ['with', 'using'], GameObject],
            'action': 'attack',
            'primary': 0,
            'secondary': None
        },
    ],
    'throw': [
        {
            'tokens': [held],
            'action': 'drop',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [held, ['on', 'to', 'at'], GameObject],
            'action': 'throw',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [held, ['away']],
            'action': 'drop',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [['away'], held],
            'action': 'drop',
            'primary': 1,
            'secondary': None
        },
    ],
    'wait': [
        {
            'tokens': [],
            'action': 'wait',
            'primary': None,
            'secondary': None
        }
    ],
    'ask': [
        {
            'tokens': [],
            'action': 'ask',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [GameObject],
            'action': 'ask',
            'primary': 0,
            'secondary': None
        },
    ],
    'tell': [
        {
            'tokens': [],
            'action': 'tell',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [GameObject],
            'action': 'tell',
            'primary': 0,
            'secondary': None
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

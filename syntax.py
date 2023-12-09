from game_object import GameObject
from lexicon import prepositions as preposition

game_object = [GameObject('', '')]
held = [GameObject('', '')]

syntax_rules = {
    'get': [
        {
            'tokens': [game_object],
            'action': 'take',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [game_object, ['from'], game_object],
            'action': 'take',
            'primary': 0,
            'secondary': 2
        },
        {
            'tokens': [game_object, ['off', 'out'], ['from', 'of'], game_object],
            'action': 'take',
            'primary': 0,
            'secondary': 3
        },
        {
            'tokens': [['to', 'in', 'into', 'at'], game_object],
            'action': 'go',
            'primary': 1,
            'secondary': None
        },
        {
            'tokens': [['to', 'in', 'into', 'at'], game_object, ['from', 'through', 'by', 'using'], game_object],
            'action': 'go',
            'primary': 1,
            'secondary': 3
        },
        {
            'tokens': [['from', 'through', 'by', 'using'], game_object, ['to', 'in', 'into', 'at'], game_object],
            'action': 'go',
            'primary': 3,
            'secondary': 1
        },
        {
            'tokens': [['through'], game_object],
            'action': 'exit',
            'primary': 1,
            'secondary': None
        },
        {
            'tokens': [['out'], ['of'], game_object],
            'action': 'exit',
            'primary': 2,
            'secondary': None
        },
        {
            'tokens': [['out'], ['of'], game_object, ['from', 'through', 'by', 'using'], game_object],
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
            'tokens': [game_object],
            'action': 'take',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [game_object, ['from', 'off', 'away', 'out'], game_object],
            'action': 'take',
            'primary': 0,
            'secondary': 2
        },
        {
            'tokens': [game_object, ['off', 'out'], ['from', 'off', 'of'], game_object],
            'action': 'take',
            'primary': 0,
            'secondary': 3
        }
    ],
    'pick': [
        {
            'tokens': [game_object],
            'action': 'unlock',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [game_object, ['with', 'using'], game_object],
            'action': 'unlock',
            'primary': 0,
            'secondary': 2
        },
        {
            'tokens': [['up'], game_object],
            'action': 'take',
            'primary': 1,
            'secondary': None
        },
        {
            'tokens': [game_object, ['up']],
            'action': 'take',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [['up'], game_object, ['from'], game_object],
            'action': 'take',
            'primary': 1,
            'secondary': 3
        },
        {
            'tokens': [['up'], game_object, ['off', 'out'], ['from', 'of'], game_object],
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
            'tokens': [held, preposition, game_object],
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
            'tokens': [held, preposition, game_object],
            'action': 'use',
            'primary': 0,
            'secondary': 2
        }
    ],
    'go': [
        {
            'tokens': [game_object],
            'action': 'go',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [['to', 'in', 'into', 'at'], game_object],
            'action': 'go',
            'primary': 1,
            'secondary': None
        },
        {
            'tokens': [game_object, ['from', 'through', 'by', 'using'], game_object],
            'action': 'go',
            'primary': 0,
            'secondary': 2
        },
        {
            'tokens': [['to', 'in', 'into', 'at'], game_object, ['from', 'through', 'by', 'using'], game_object],
            'action': 'go',
            'primary': 1,
            'secondary': 3
        },
        {
            'tokens': [['from', 'through', 'by', 'using'], game_object, ['to', 'in', 'into', 'at'], game_object],
            'action': 'go',
            'primary': 3,
            'secondary': 1
        },
        {
            'tokens': [['from', 'through', 'by', 'using'], game_object],
            'action': 'exit',
            'primary': 1,
            'secondary': None
        },
        {
            'tokens': [['out'], ['of'], game_object],
            'action': 'exit',
            'primary': 2,
            'secondary': None
        },
        {
            'tokens': [['out'], ['of'], game_object, ['from', 'through', 'by', 'using'], game_object],
            'action': 'exit',
            'primary': 2,
            'secondary': 4
        }
    ],
    'enter': [
        {
            'tokens': [game_object],
            'action': 'enter',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [['to', 'in', 'into', 'at'], game_object],
            'action': 'enter',
            'primary': 1,
            'secondary': None
        },
        {
            'tokens': [game_object, ['from', 'through', 'by', 'using'], game_object],
            'action': 'go',
            'primary': 0,
            'secondary': 2
        },
        {
            'tokens': [['to', 'in', 'into', 'at'], game_object, ['from', 'through', 'by', 'using'], game_object],
            'action': 'go',
            'primary': 1,
            'secondary': 3
        },
        {
            'tokens': [['from', 'through', 'by', 'using'], game_object, ['to', 'in', 'into', 'at'], game_object],
            'action': 'go',
            'primary': 3,
            'secondary': 1
        },
        {
            'tokens': [['from', 'through', 'by', 'using'], game_object],
            'action': 'exit',
            'primary': 1,
            'secondary': None
        }
    ],
    'exit': [
        {
            'tokens': [game_object],
            'action': 'exit',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [['to', 'in', 'into', 'at'], game_object],
            'action': 'go',
            'primary': 1,
            'secondary': None
        },
        {
            'tokens': [game_object, ['from', 'through', 'by', 'using'], game_object],
            'action': 'exit',
            'primary': 0,
            'secondary': 2
        },
        {
            'tokens': [['to', 'in', 'into', 'at'], game_object, ['from', 'through', 'by', 'using'], game_object],
            'action': 'go',
            'primary': 1,
            'secondary': 3
        },
        {
            'tokens': [['from', 'through', 'by', 'using'], game_object, ['to', 'in', 'into', 'at'], game_object],
            'action': 'go',
            'primary': 3,
            'secondary': 1
        },
        {
            'tokens': [['from', 'through', 'by', 'using'], game_object],
            'action': 'exit',
            'primary': 1,
            'secondary': None
        }
    ],
    'leave': [
        {
            'tokens': [game_object],
            'action': 'leave',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [['to', 'in', 'into', 'at'], game_object],
            'action': 'go',
            'primary': 1,
            'secondary': None
        },
        {
            'tokens': [game_object, ['from', 'through', 'by', 'using'], game_object],
            'action': 'exit',
            'primary': 0,
            'secondary': 2
        },
        {
            'tokens': [held, ['in', 'at', 'on', 'to', 'into', 'onto'], game_object],
            'action': 'drop',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [['to', 'in', 'into', 'at'], game_object, ['from', 'through', 'by', 'using'], game_object],
            'action': 'go',
            'primary': 1,
            'secondary': 3
        },
        {
            'tokens': [['from', 'through', 'by', 'using'], game_object, ['to', 'in', 'into', 'at'], game_object],
            'action': 'go',
            'primary': 3,
            'secondary': 1
        },
        {
            'tokens': [['from', 'through', 'by', 'using'], game_object],
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
            'tokens': [game_object],
            'action': 'examine',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [preposition, game_object],
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
            'tokens': [game_object],
            'action': 'lock',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [game_object, ['with', 'using'], held],
            'action': 'lock',
            'primary': 0,
            'secondary': 2
        },
    ],
    'unlock': [
        {
            'tokens': [game_object],
            'action': 'unlock',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [game_object, ['with', 'using'], held],
            'action': 'unlock',
            'primary': 0,
            'secondary': 2
        },
    ],
    'open': [
        {
            'tokens': [game_object],
            'action': 'open',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [game_object, ['with', 'using'], held],
            'action': 'open',
            'primary': 0,
            'secondary': 2
        },
    ],
    'close': [
        {
            'tokens': [game_object],
            'action': 'close',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [game_object, ['with', 'using'], game_object],
            'action': 'close',
            'primary': 0,
            'secondary': 2
        },
    ],
    'wake': [
        {
            'tokens': [game_object],
            'action': 'wake',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [game_object, ['up']],
            'action': 'wake',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [['up'], game_object],
            'action': 'wake',
            'primary': 1,
            'secondary': None
        },
    ],
    'attack': [
        {
            'tokens': [game_object],
            'action': 'attack',
            'primary': 0,
            'secondary': None
        },
        {
            'tokens': [game_object, ['with', 'using'], game_object],
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
            'tokens': [held, ['on', 'to', 'at'], game_object],
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
            'tokens': [game_object],
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
            'tokens': [game_object],
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

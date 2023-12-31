stop_words = ['the', 'a', 'an',
              'this', 'that', 'these', 'those',
              'my', 'your', 'his', 'her', 'its', 'our', 'their'
              'one', 'again', 'back', 'carefully', 'caution']

prepositions = ['in', 'at', 'on', 'up', 'to', 'off',
                'of', 'from', 'with', 'out', 'away',
                'into', 'onto', 'through', 'by', 'around',
                'closely', 'using', 'outside', 'beside', 'near', 'towards']

pronouns = ['him', 'her', 'it', 'them']

verbs = {
    'go': {
        'synonyms': ['access', 'move', 'walk', 'travel', 'proceed', 'navigate', 'pass']
    },
    'exit': {
        'synonyms': ['depart', 'withdraw', 'evacuate', 'retreat', 'escape', 'flee']
    },
    'take': {
        'synonyms': ['steal', 'grab', 'acquire', 'collect', 'obtain', 'fetch', 'retrieve', 'remove', 'reach', 'pull']
    },
    'drop': {
        'synonyms': ['release', 'discard', 'let', 'abandon']
    },
    'enter': {
        'synonyms': ['hide', 'climb']
    },
    'use': {
        'synonyms': ['utilize', 'apply', 'operate', 'test']
    },
    'examine': {
        'synonyms': ['search', 'look', 'investigate', 'inspect', 'analyze', 'approach',
                     'survey', 'check', 'explore', 'observe', 'scan', 'peek', 'see']
    },
    'lock': {
        'synonyms': ['seal']
    },
    'unlock': {
        'synonyms': []
    },
    'open': {
        'synonyms': ['unseal']
    },
    'close': {
        'synonyms': ['shut']
    },
    'wake': {
        'synonyms': ['awaken']
    },
    'attack': {
        'synonyms': ['assault', 'fight', 'confront', 'hit', 'strike']
    },
    'throw': {
        'synonyms': ['shoot', 'launch', 'toss']
    },
    'ask': {
        'synonyms': ['inquire']
    },
    'tell': {
        'synonyms': ['order', 'demand']
    },
    'wait': {'synonyms': []},
    'help': {'synonyms': []},
    'get': {'synonyms': []},
    'pick': {'synonyms': []},
    'leave': {'synonyms': []},
    'step': {'synonyms': []},
}

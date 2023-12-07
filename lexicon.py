stop_words = ['the', 'a', 'an', 'and',
              'this', 'that', 'these', 'those',
              'my', 'your', 'his', 'her', 'its', 'our', 'their'
              'one']

prepositions = ['in', 'at', 'on', 'up', 'to', 'off',
                'of', 'from', 'with', 'out', 'away',
                'into', 'onto', 'through', 'by', 'around',
                'closely', 'using']

pronouns = ['him', 'her', 'it', 'them']

verbs = {
    'go': {
        'synonyms': ['access', 'move', 'walk', 'travel', 'proceed', 'navigate', 'pass']
    },
    'exit': {
        'synonyms': ['depart', 'withdraw', 'evacuate', 'retreat', 'escape', 'flee']
    },
    'take': {
        'synonyms': ['steal', 'grab', 'acquire', 'collect', 'obtain', 'fetch', 'retrieve']
    },
    'drop': {
        'synonyms': ['release', 'discard', 'let', 'abandon']
    },
    'enter': {
        'synonyms': ['hide']
    },
    'use': {
        'synonyms': ['utilize', 'apply', 'operate', 'test']
    },
    'examine': {
        'synonyms': ['search', 'look', 'investigate', 'inspect', 'analyze',
                     'survey', 'check', 'explore', 'observe', 'scan']
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
        'synonyms': ['assault', 'fight', 'confront']
    },
    'throw': {
        'synonyms': ['shoot', 'launch', 'strike', 'toss']
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
}

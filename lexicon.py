stop_words = ['the', 'a', 'an', 'and',
              'this', 'that', 'these', 'those',
              'my', 'your', 'his', 'her', 'its', 'our', 'their'
              'one']

prepositions = ['in', 'at', 'on', 'up', 'to', 'off',
                'of', 'from', 'with', 'out', 'away',
                'into', 'onto', 'through', 'by',
                'using']

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
        'synonyms': ['utilize', 'apply', 'operate']
    },
    'examine': {
        'synonyms': ['search', 'look', 'investigate', 'inspect', 'analyze', 'survey']
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
        'synonyms': ['assault', 'strike', 'fight', 'confront']
    },
    'ask': {
        'synonyms': ['inquire']
    },
    'tell': {
        'synonyms': ['order', 'demand']
    },
    'throw': {
        'synonyms': ['shoot', 'launch']
    },
    'wait': {
        'synonyms': ['stand']
    },
    'help': {
        'synonyms': []
    },
    'get': {'synonyms': []},
    'pick': {'synonyms': []},
    'leave': {'synonyms': []},
}

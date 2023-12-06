stop_words = ['the', 'a', 'an', 'and']

prepositions = ['in', 'at', 'on', 'up', 'to', 'of', 'from', 'with']

available_verbs = {
    "go": {
        "synonyms": ["access", "move", "walk", "travel",
                     "proceed", "navigate"]
    },
    "exit": {
        "synonyms": ["depart", "leave", "withdraw", "evacuate",
                     "retreat", "escape", "flee"]
    },
    "examine": {
        "synonyms": ["search", "look", "investigate", "inspect",
                     "analyze", "survey"]
    },
    "take": {
        "synonyms": ["steal", "grab", "acquire", "pick",
                     "collect", "seize"]
    },
    "drop": {
        "synonyms": ["release", "discard", "let", "abandon"]
    },
    "enter": {
        "synonyms": ["hide"]
    },
    "use": {
        "synonyms": ["utilize", "apply", "operate"]
    },
    "lock": {
        "synonyms": ["seal"]
    },
    "unlock": {
        "synonyms": ["pick"]
    },
    "open": {
        "synonyms": ["unseal"]
    },
    "close": {
        "synonyms": ["shut"]
    },
    "wake": {
        "synonyms": ["awaken"]
    },
    "attack": {
        "synonyms": ["assault", "strike", "fight", "confront"]
    },
    "ask": {
        "synonyms": ["inquire"]
    },
    "tell": {
        "synonyms": ["order", "demand"]
    },
    "throw": {
        "synonyms": ["shoot", "launch"]
    },
    "wait": {
        "synonyms": ["stand"]
    },
    "help": {
        "synonyms": []
    }
}

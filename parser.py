from lexicon import available_verbs, stop_words, prepositions, game_objects_dict
from outcomes import AMBIGUOUS_OBJECTS, INVALID_COMMAND, INVALID_OBJECTS, Outcome
from result import Result
from world import World


def is_verb(word):
    return word in available_verbs.keys()


def is_preposition(word):
    return word in prepositions


class Parser:
    def __init__(self, world, input_command, silent=False, advance_time=True):
        self.world = world
        self.input_command = input_command
        self.silent = silent
        self.advance_time = advance_time

        self.lexicon = world.get_game_object_lexicon()
        self.wn = 2
        self.words_list = [word for word in input_command.strip().lower().split() if word not in stop_words]
        self.verb = self.parse_verb()
        self.identified_tokens = []
        self.next_identified_object = None

    def parse(self):
        # for testing
        print(self.words_list)

        if not self.words_list:
            print("You choose to remain silent.")
            return Result(None, None)

        # Check if asked for help

        #  Lexical analysis
        print("Verb-> " + self.verb)
        while self.wn <= len(self.words_list):
            parse_outcome = self.parse_objects()
            if parse_outcome in (INVALID_COMMAND, INVALID_OBJECTS, AMBIGUOUS_OBJECTS):
                outcome = Outcome(parse_outcome)

        # Test print tokens
        identified_token_names = []
        for token in self.identified_tokens:
            if token in prepositions:
                identified_token_names.append(token)
            else:
                identified_token_names.append(token.long)
        print(identified_token_names)

        #  Syntax analysis

    def next_word(self):
        words = self.words_list

        if self.wn > len(words):
            return None
        nextword = words[self.wn - 1]
        self.wn += 1

        return nextword

    def parse_verb(self):
        words = self.words_list

        if not words:
            return None

        verb = words[0]
        if not is_verb(verb):
            for key, value in available_verbs.items():
                if words[0] in value["synonyms"]:
                    # If a synonym is found, return the corresponding verb
                    verb = key

        return verb

    def there_is_ambiguity(self):
        for value in self.lexicon.values():
            if value['score'] > 0:
                scores_are_not_zero = True
                break
        else:
            scores_are_not_zero = False
        return self.next_identified_object is None and scores_are_not_zero

    def reset_scores(self):
        self.lexicon = self.world.get_game_object_lexicon()

    def append_token_with_max_score(self):
        self.identified_tokens.append(self.next_identified_object)
        self.reset_scores()
        self.next_identified_object = None

    def parse_objects(self):
        word = self.next_word()
        if word is None:
            if self.there_is_ambiguity():
                return AMBIGUOUS_OBJECTS
            if self.next_identified_object:
                self.identified_tokens.append(self.next_identified_object)
            return 1

        # Process next token
        if is_verb(word):
            return INVALID_COMMAND

        if is_preposition(word):
            if self.next_identified_object:
                self.append_token_with_max_score()
            elif self.there_is_ambiguity():
                return AMBIGUOUS_OBJECTS

            self.identified_tokens.append(word)
            return 1

        # There's already a unique object identified whose score is max
        if self.next_identified_object:
            if word in self.lexicon[self.next_identified_object]['long']:
                self.lexicon[self.next_identified_object]['score'] += 1
                return 1
            else:
                self.append_token_with_max_score()

        invalid_objects = True
        # Begin to identify the next token
        for obj, value in self.lexicon.items():
            if word in obj['long']:
                obj['score'] += 1
                invalid_objects = False

        if invalid_objects:
            return INVALID_OBJECTS

        max_score = max((obj['score'] for obj in self.lexicon.values()), default=None)
        max_score_objects = [obj for obj in self.lexicon.values() if obj['score'] == max_score]

        if len(max_score_objects) == 1:
            self.next_identified_object = max_score_objects[0]

        return 1


w = World()
w.populate()
print("\nWhat do you want to do?")
command = input("> ")
parser = Parser(w, command)
parser.parse()

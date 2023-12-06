from lexicon import available_verbs, stop_words, prepositions
from outcomes import AMBIGUOUS_OBJECTS, INVALID_COMMAND, INVALID_OBJECTS, Outcome, INVALID_VERB
from result import Result
from world import World


def is_verb(word):
    return is_main_verb(word) or synonym_of(word) is not None


def is_main_verb(word):
    return word in available_verbs.keys()


def synonym_of(verb):
    for key, value in available_verbs.items():
        if verb in value["synonyms"]:
            return key
    return None


def is_preposition(word):
    return word in prepositions


class Parser:
    def __init__(self, world, input_command, silent=False, advance_time=True):
        self.world = world
        self.input_command = input_command
        self.silent = silent
        self.advance_time = advance_time

        self.game_objects_dictionary = world.get_game_objects_dict()
        self.wn = 2
        self.verb = None
        self.words = [word for word in input_command.strip().lower().split() if word not in stop_words]
        self.identified_tokens = []
        self.next_identified_object = None

        self.debugging = True

    # Debugging methods
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def debug(self, message=""):
        if self.debugging:
            print(message)

    def show_game_object_dict(self):
        if not self.debugging:
            return
        for key, value in self.game_objects_dictionary.items():
            if value['score'] > 0:
                print(f"{key}: {value}")
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Parsing methods
    def parse(self):
        self.debug(f"Words: {self.words}")

        if not self.words:
            print("You choose to remain silent.")
            return Result(None, None)

        # Check if asked for help

        # LEXICAL ANALYSIS
        # Parse verb
        self.verb = self.parse_verb()
        if self.verb is None:
            outcome = Outcome(INVALID_VERB)
            print(outcome.description)
            return
        self.debug(f"Verb: {self.verb}")
        self.debug()

        # TODO Take player's scope into account

        # Parse objects
        while self.wn <= len(self.words) + 1:
            self.debug(f"Iteration of word No{self.wn}")
            self.debug("-------------------------------")
            self.debug(f"wn: {self.wn} <= len(words) + 1: {len(self.words) + 1}")
            outcome = self.parse_objects()
            if outcome in (INVALID_COMMAND, INVALID_VERB, INVALID_OBJECTS, AMBIGUOUS_OBJECTS):
                outcome = Outcome(outcome)
                print(outcome.description)
                return
            self.show_game_object_dict()
            self.debug()

        self.debug(f"Identified tokens: {[token if is_preposition(token) else token.name for token in self.identified_tokens]}")

        # TODO SYNTAX ANALYSIS
        # SYNTAX ANALYSIS
        # for rule in syntax_rules[verb]:
        #     if match_rule(tokens, rule):
        #         action = rule[action]
        # primary_object = tokens[rule[primary_object]]
        # secondary_object = tokens[rule[secondary_object]]
        # action(primary_object, secondary_object)
        # get result
        # show result
        # advance time

        # def match_rule(tokens, rule):
        #     if len(tokens) != len(rule[tokens]):
        #         return False
        #
        # for i in range(len(tokens)):
        #     if not match_token(tokens[i], rule[tokens][i])
        #         return False
        # return True
        #
        # def match_token(token, rule_token):
        #     if isinstance(token, str):
        #         return (isinstance(rule_token, str) and token == rule_token) or
        #         (isinstance(rule_token, list) and token in rule_token)
        #
        # else:  # if token is a GameObject
        # return isinstance(token, rule_token)

    def next_word(self):
        self.debug("next_word() is called")
        if self.wn > len(self.words):
            self.debug(f"wn: {self.wn} > len(words): {len(self.words)}")
            self.wn += 1
            return None

        nextword = self.words[self.wn - 1]
        self.debug(f"nextword = '{nextword}'")
        self.wn += 1
        self.debug(f"wn is increased to {self.wn}")
        return nextword

    def parse_verb(self):
        verb = self.words[0]
        if not is_main_verb(verb):
            return synonym_of(verb)
        return verb

    def there_is_unique_identified_object(self):
        if self.next_identified_object is not None:
            self.debug(f"There is currently a unique identified object: {self.next_identified_object.name}")
            return True
        else:
            self.debug(f"There is NOT a unique identified object")
            return False

    def there_is_ambiguity(self):
        for key, value in self.game_objects_dictionary.items():
            if value['score'] > 0:
                self.debug(f"The score of '{key.name}' is found to be {value['score']} > 0")
                all_scores_are_zero = False
                break
        else:
            all_scores_are_zero = True
        return not (self.there_is_unique_identified_object() or all_scores_are_zero)

    def reset_scores(self):
        self.game_objects_dictionary = self.world.get_game_objects_dict()

    def append_token_with_max_score(self):
        self.identified_tokens.append(self.next_identified_object)
        self.debug(f"'{self.next_identified_object.name}' is appended to identified tokens list")
        self.reset_scores()
        self.next_identified_object = None
        self.debug(f"next_identified_object is reset to None")

    def parse_objects(self):
        word = self.next_word()

        # Reached end of input
        if word is None:
            self.debug("Reached end of input")
            if self.there_is_ambiguity():
                return AMBIGUOUS_OBJECTS
            if self.there_is_unique_identified_object():
                self.append_token_with_max_score()
            return 1

        # A word, other than the first, is a verb
        if is_verb(word):
            self.debug(f"A word ('{word}'), other than the first, is a verb")
            return INVALID_COMMAND

        # A preposition is found
        if is_preposition(word):
            self.debug(f"A preposition is found: '{word}'")
            if self.there_is_unique_identified_object():
                self.append_token_with_max_score()
            elif self.there_is_ambiguity():
                return AMBIGUOUS_OBJECTS

            self.identified_tokens.append(word)
            self.debug(f"'{word}' is appended to identified tokens list")
            return 1

        if self.there_is_unique_identified_object():
            if word in self.game_objects_dictionary[self.next_identified_object]['long']:
                self.debug(f"'{word}' is in {self.next_identified_object}'s long name ('{self.next_identified_object.long}')")
                self.game_objects_dictionary[self.next_identified_object]['score'] += 1
                self.debug(f"{self.next_identified_object}'s score is increased to {self.game_objects_dictionary[self.next_identified_object]['score']}")
                return 1
            else:
                self.append_token_with_max_score()

        # Parse next object
        invalid_objects = True
        for key, value in self.game_objects_dictionary.items():
            if word in value['long']:
                self.debug(f"'{word}' is in {key}'s long name ('{key.long}')")
                value['score'] += 1
                self.debug(f"{key}'s score is increased to {value['score']}")
                invalid_objects = False
        if invalid_objects:
            self.debug(f"No object has '{word}' in its long name")
            return INVALID_OBJECTS

        max_score = max((obj['score'] for obj in self.game_objects_dictionary.values()), default=None)
        self.debug(f"Max score is: {max_score}")
        max_score_objects = [key for key, obj in self.game_objects_dictionary.items() if obj['score'] == max_score]
        self.debug(f"Objects with max score: {[obj.name for obj in max_score_objects]}")

        if len(max_score_objects) == 1:
            self.debug("A unique object has the max score")
            self.next_identified_object = max_score_objects[0]
            self.debug(f"next_identified_object is set to {max_score_objects[0]}")

        return 1


w = World()
w.populate()
print()
command = "grab lockpick with"
print(f"Command: {command}")
parser = Parser(w, command)
parser.parse()

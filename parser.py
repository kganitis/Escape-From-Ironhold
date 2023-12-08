from actions import Action
from lexicon import verbs, stop_words, prepositions
from outcomes import AMBIGUOUS_OBJECTS, INVALID_COMMAND, INVALID_OBJECTS, Outcome, INVALID_VERB, OUT_OF_SCOPE, NEUTRAL, \
    TRANSFORMED, FAIL, INVALID_SYNTAX
from result import Result
from syntax import syntax_rules


def is_verb(word):
    return is_main_verb(word) or synonym_of(word) is not None


def is_main_verb(word):
    return word in verbs.keys()


def synonym_of(verb):
    for key, value in verbs.items():
        if verb in value["synonyms"] or verb == key:
            return key
    return None


def is_preposition(word):
    return word in prepositions


def show_help():
    print(f"Main verbs: {list(verbs.keys())}")


class Parser:
    def __init__(self, world, input_command, silent=False, advance_time=True):
        self.world = world
        self.input_command = input_command
        self.silent = silent
        self.advance_time = advance_time

        self.game_objects_dictionary = None
        self.wn = 2
        self.input_verb = None
        self.verb = None
        self.action_verb = None
        self.words = [word for word in input_command.strip().lower().split() if word not in stop_words]
        self.identified_tokens = []
        self.next_identified_object = None
        self.ambiguous_objects = []

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
            return

        # LEXICAL ANALYSIS
        # Parse verb
        self.parse_verb()
        if self.verb is None:
            outcome = Outcome(INVALID_VERB)
            print(outcome.formatted_description)
            return
        self.debug(f"Verb: {self.verb}")
        self.debug()

        # Check if asked for help
        if self.verb == 'help':
            show_help()
            return

        # Parse objects
        self.game_objects_dictionary = self.world.get_game_objects_dict()
        while self.wn <= len(self.words) + 1:
            self.debug(f"Iteration of word No{self.wn}")
            self.debug("-------------------------------")
            self.debug(f"wn: {self.wn} <= len(words) + 1: {len(self.words) + 1}")

            outcome = self.parse_objects()

            # Check command validity
            if outcome in (INVALID_COMMAND, INVALID_VERB, INVALID_OBJECTS):
                outcome = Outcome(outcome, self.verb)
                print(outcome.formatted_description)
                return

            # Check ambiguity
            if outcome == AMBIGUOUS_OBJECTS:
                outcome = Outcome(outcome, self.verb, ambiguous_objects=self.ambiguous_objects)
                print(outcome.formatted_description)
                return

            # Check player's scope
            if self.there_is_unique_identified_object():
                if self.next_identified_object not in self.world.player.scope:
                    outcome = Outcome(OUT_OF_SCOPE, self.verb, self.next_identified_object)
                    print(outcome.formatted_description)
                    return

            self.show_game_object_dict()
            self.debug()

        self.debug(f"Identified tokens: {[token if is_preposition(token) else '<' + token.name + '>' for token in self.identified_tokens]}")

        # SYNTAX ANALYSIS
        for rule in syntax_rules[self.verb]:
            if self.match_rule(rule):
                self.action_verb = rule['action']
                primary_object = self.identified_tokens[rule['primary']] if rule['primary'] is not None else None
                secondary_object = self.identified_tokens[rule['secondary']] if rule['secondary'] is not None else None
                action = Action(self.world, self.input_verb, self.action_verb, primary_object, secondary_object)
                outcome = action.execute()
                result = Result(action, outcome)
                self.debug(f"Action verb: {self.action_verb}")
                self.debug(f"Primary: {primary_object}")
                self.debug(f"Secondary: {secondary_object}")
                break
        else:
            outcome = Outcome(INVALID_SYNTAX)
            print(outcome.formatted_description)
            return

        # Print
        if not self.silent:
            result.show()

        # Move end - advance time
        actions_not_advancing_time = ['examine']
        outcomes_not_advancing_time = [INVALID_COMMAND, NEUTRAL, FAIL, TRANSFORMED]
        if self.verb not in actions_not_advancing_time \
                and outcome.type not in outcomes_not_advancing_time \
                and self.advance_time:
            self.world.on_move_end()

        return result

    def match_rule(self, rule):
        if len(self.identified_tokens) != len(rule['tokens']):
            return False

        for i in range(len(self.identified_tokens)):
            if not self.match_token(self.identified_tokens[i], rule['tokens'][i]):
                return False
        return True

    def match_token(self, identified_token, rule_token):
        if isinstance(identified_token, str):
            return isinstance(rule_token, list) and identified_token in rule_token
        else:  # if it's game object
            return isinstance(identified_token, rule_token)

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
        synonym = synonym_of(verb)
        if is_main_verb(verb) or synonym is not None:
            self.input_verb = verb
            self.verb = synonym

    def there_is_unique_identified_object(self):
        if self.next_identified_object is not None:
            self.debug(f"There is currently a unique identified object: {self.next_identified_object.name}")
            return True
        else:
            self.debug(f"There is NOT a unique identified object")
            return False

    def check_ambiguity(self):
        if self.there_is_unique_identified_object():
            return False

        max_score = max((obj['score'] for obj in self.game_objects_dictionary.values()), default=None)
        self.debug(f"Max score is: {max_score}")
        if max_score == 0:
            return False

        max_score_objects = [key for key, obj in self.game_objects_dictionary.items() if obj['score'] == max_score]
        self.debug(f"Objects with max score: {[obj.name for obj in max_score_objects]}")
        in_scope_objects = [obj for obj in max_score_objects if self.game_objects_dictionary[obj]['in scope']]
        self.debug(f"Objects in scope: {[obj.name for obj in in_scope_objects]}")
        out_of_scope_objects = [obj for obj in max_score_objects if not self.game_objects_dictionary[obj]['in scope']]
        self.debug(f"Objects out of scope: {[obj.name for obj in out_of_scope_objects]}")

        if len(in_scope_objects) == 1:
            self.next_identified_object = in_scope_objects[0]
            return False

        self.ambiguous_objects = in_scope_objects if in_scope_objects != [] else out_of_scope_objects
        return True

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
            if self.check_ambiguity():
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
            if self.check_ambiguity():
                return AMBIGUOUS_OBJECTS
            if self.there_is_unique_identified_object():
                self.append_token_with_max_score()

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


# TODO Finally:
#  Define special syntax rules for 'ask' and 'tell' ("ask/tell {anything}") --> how to represent {anything}
#  Support pronouns ('him', 'her', 'it', 'them')
#  Parse verb until a verb is found
#  Ambiguity resolution
#  Generate multiple actions from one command ("unlock the door with lockpick, then open it and exit the cell")
#  How to handle "use the key to unlock the door"

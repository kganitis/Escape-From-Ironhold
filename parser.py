import string

from actions import Action
from lexicon import verbs, stop_words, prepositions, pronouns
from outcomes import *
from result import Result
from syntax import syntax_rules, held, game_object


# TODO Generate multiple actions from one command ("unlock the door with lockpick, then open it and exit the cell")


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
        self.wn = 1
        self.input_verb = None
        self.verb = None
        self.action_verb = None

        self.clear_input()

        self.identified_tokens = []
        self.ambiguous_objects = []

        self.debugging = False

    def clear_input(self):
        # Remove apostrophes and handle possessive forms
        cleaned_input = self.input_command.replace("'", ' ').replace("’", ' ')

        # Remove punctuation and lowercase words
        translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
        cleaned_words = [word.translate(translator) for word in cleaned_input.strip().lower().split()]

        # Filter out stop words
        self.words = [word for word in cleaned_words if word not in stop_words and len(word) > 1]

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
        result = self.__parse()

        if not self.silent:
            result.show()

        # Move end - advance time
        actions_not_advancing_time = ['examine', 'help']
        outcomes_not_advancing_time = [INVALID, NEUTRAL, FAIL, AMBIGUOUS, TRANSFORMED]
        if self.advance_time \
                and self.verb not in actions_not_advancing_time \
                and result.outcome.type not in outcomes_not_advancing_time:
            self.world.on_move_end()

        return result

    def __parse(self):
        self.debug(f"Words: {self.words}")

        if not self.words:
            print("You choose to remain silent.")
            return

        print(self.words)

        # LEXICAL ANALYSIS
        # Parse verb
        for _ in self.words:
            self.parse_verb()
            if self.verb:
                break
        else:
            # it's ok to skip the verb if we're in resolve ambiguity mode, just reset wn to 1
            if self.ambiguous_objects:
                self.wn = 1
            else:
                outcome = Outcome(INVALID_VERB)
                return Result(None, outcome)
        self.debug(f"Verb: {self.verb}")
        self.debug()

        # Check if asked for help
        if self.verb == 'help':
            show_help()
            outcome = Outcome(NO_MESSAGE)
            return Result(None, outcome)

        # Parse objects
        self.game_objects_dictionary = self.world.get_game_objects_dict(for_objects=self.ambiguous_objects)
        while self.wn <= len(self.words) + 1:
            self.debug(f"Iteration of word No{self.wn}")
            self.debug("-------------------------------")
            self.debug(f"wn: {self.wn} <= len(words) + 1: {len(self.words) + 1}")

            outcome = self.parse_objects()

            # Check command validity
            if outcome in (INVALID_COMMAND, INVALID_VERB, INVALID_OBJECTS):
                outcome = Outcome(outcome, self.verb)
                return Result(None, outcome)

            self.show_game_object_dict()
            self.debug()

        self.debug(f"Identified tokens: {self.identified_tokens}")

        # SYNTAX ANALYSIS
        # First special rules for 'wait', 'ask', 'tell'
        if self.verb in ['wait', 'ask', 'tell']:
            primary_object = secondary_object = None
            if self.verb in ['ask', 'tell']:
                if self.identified_tokens and not isinstance(self.identified_tokens[0], str):
                    primary_object = self.identified_tokens[0]
            action = Action(self.world, self.input_verb, self.verb, primary_object, secondary_object)
            outcome = action.execute()
            return Result(action, outcome)

        # Match verb and identified tokens with an existing syntax rule
        action = None
        for rule in syntax_rules[self.verb]:
            action = None
            match = self.match_rule(rule)
            if match:
                if match == "PERFECT" and not self.ambiguous_objects:
                    self.action_verb = rule['action']
                    primary_object = self.identified_tokens[rule['primary']] if rule['primary'] is not None else None
                    secondary_object = self.identified_tokens[rule['secondary']] if rule['secondary'] is not None else None
                    second_verb = self.identified_tokens[rule['verb']] if 'verb' in rule.keys() else None
                    action = Action(self.world, self.input_verb, self.action_verb, primary_object, secondary_object, second_verb)
                    outcome = action.execute()
                else:
                    outcome = match
                break
        else:
            outcome = Outcome(INVALID_SYNTAX)

        return Result(action, outcome)

    def match_rule(self, rule):
        if len(self.identified_tokens) != len(rule['tokens']):
            return False
        match = "PERFECT"
        for i in range(len(self.identified_tokens)):
            match = self.match_token(i, self.identified_tokens[i], rule['tokens'][i])
            if not match:
                return False
        return match

    def match_token(self, wn, identified_tokens, rule_tokens):
        self.debug(f"Comparing {identified_tokens} with {rule_tokens}")
        PERFECT_MATCH = "PERFECT"
        if isinstance(identified_tokens, str):
            identified_tokens = [identified_tokens]
            self.debug(f"identified_tokens is just a single string and I'm converting it to a list: {identified_tokens}")

        if not isinstance(identified_tokens[0], type(rule_tokens[0])):
            self.debug("identified_tokens and rule_tokens contain different types of elements:")
            self.debug(f"Type of identified_tokens: {type(identified_tokens[0])}")
            self.debug(f"Type of rule_tokens: {type(rule_tokens[0])}")
            return False

        if rule_tokens == game_object:
            self.debug(f"Check for objects in scope")
            rule_tokens = self.world.player.scope
            self.debug(f"Objects in scope: {rule_tokens}")
            common_tokens = [token for token in identified_tokens if token in rule_tokens]
            self.debug(f"Common tokens: {common_tokens}")

            if len(common_tokens) > 1:
                self.debug("There's ambiguity")
                self.debug(f"Ambiguous tokens: {common_tokens}")
                self.debug(f"Resolve ambiguity")
                self.debug(f"Replace token in position {wn} of identified_tokens with the clarified token:")
                self.identified_tokens[wn] = self.parse_ambiguous(common_tokens)
                self.debug(f"New identified tokens list: {self.identified_tokens}")
                return PERFECT_MATCH
            elif len(common_tokens) == 1:
                self.debug(f"Replace the object list in position {wn} of identified_tokens with the unique common token: {common_tokens[0]}")
                self.identified_tokens[wn] = common_tokens[0]
                self.debug(f"New identified tokens list: {self.identified_tokens}")
                return PERFECT_MATCH

            # No common tokens
            if len(identified_tokens) > 1:
                self.debug("There's ambiguity")
                self.debug(f"Ambiguous tokens: {common_tokens}")
                self.debug(f"Resolve ambiguity")
                self.debug(f"Replace token in position {wn} of identified_tokens with the clarified token:")
                self.identified_tokens[wn] = self.parse_ambiguous(common_tokens)
                self.debug(f"New identified tokens list: {self.identified_tokens}")
                return PERFECT_MATCH
            elif len(identified_tokens) == 1:
                self.debug(f"There's a unique identified token ({identified_tokens[0]}) but it's out of scope")
                self.identified_tokens[wn] = identified_tokens[0]
                return Outcome(OUT_OF_SCOPE, self.verb, identified_tokens[0])

        if rule_tokens == held:
            self.debug(f"Check for objects in held")
            rule_tokens = self.world.player.held
            self.debug(f"Objects held: {rule_tokens}")
            common_tokens = [token for token in identified_tokens if token in rule_tokens]
            self.debug(f"Common tokens: {common_tokens}")

            if len(common_tokens) > 1:
                self.debug("There's ambiguity")
                self.debug(f"Ambiguous tokens: {common_tokens}")
                self.debug(f"Resolve ambiguity")
                self.debug(f"Replace token in position {wn} of identified_tokens with the clarified token:")
                self.identified_tokens[wn] = self.parse_ambiguous(common_tokens)
                self.debug(f"New identified tokens list: {self.identified_tokens}")
                return PERFECT_MATCH
            elif len(common_tokens) == 1:
                self.debug(
                    f"Replace the object list in position {wn} of identified_tokens with the unique common token: {common_tokens[0]}")
                self.identified_tokens[wn] = common_tokens[0]
                self.debug(f"New identified tokens list: {self.identified_tokens}")
                return PERFECT_MATCH

            # No common tokens
            if len(identified_tokens) > 1:
                self.debug("There's ambiguity")
                self.debug(f"Ambiguous tokens: {common_tokens}")
                self.debug(f"Resolve ambiguity")
                self.debug(f"Replace token in position {wn} of identified_tokens with the clarified token:")
                self.identified_tokens[wn] = self.parse_ambiguous(common_tokens)
                self.debug(f"New identified tokens list: {self.identified_tokens}")
                return PERFECT_MATCH
            elif len(identified_tokens) == 1:
                self.debug(f"There's a unique identified token ({identified_tokens[0]}) but it's not in held")
                self.identified_tokens[wn] = identified_tokens[0]
                return Outcome(NOT_IN_POSSESSION, self.verb, identified_tokens[0])

        if identified_tokens[0] in rule_tokens:
            self.debug(f"{identified_tokens[0]} is in rule_tokens: {rule_tokens}")
            return PERFECT_MATCH

        self.debug(f"identified_tokens ({identified_tokens[0]}) and rule_tokens ({rule_tokens}) don't match")
        return False

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
        verb = self.next_word()
        synonym = synonym_of(verb)
        if is_main_verb(verb) or synonym is not None:
            self.input_verb = verb
            self.verb = synonym

    def reset_scores(self):
        self.game_objects_dictionary = self.world.get_game_objects_dict()

    def append_tokens_with_max_score(self):
        max_score = max((obj['score'] for obj in self.game_objects_dictionary.values()), default=None)
        if max_score > 0:
            max_score_objects = [key for key, obj in self.game_objects_dictionary.items() if obj['score'] == max_score]
            self.debug(f"Appended objects with max score: {[obj.name for obj in max_score_objects]}")
            self.identified_tokens.append(max_score_objects)
            self.reset_scores()

    def parse_objects(self):
        word = self.next_word()

        reached_end_of_input = word is None
        if reached_end_of_input:
            self.debug("Reached end of input")
            self.append_tokens_with_max_score()
            return 1

        # A word, other than the first, is a verb
        if is_verb(word):
            # it's ok to meet a verb, just return to skip over it
            return 1

        # A preposition is found
        if is_preposition(word):
            self.debug(f"A preposition is found: '{word}'")
            self.append_tokens_with_max_score()

            # if we're in resolve ambiguity mode, don't proceed to append the pronoun, just stop here
            if self.ambiguous_objects:
                return 1

            self.identified_tokens.append(word)
            self.debug(f"'{word}' is appended to identified tokens list")
            return 1

        if word in pronouns:
            self.identified_tokens.append([self.world.last_primary])
            self.debug(f"'{[self.world.last_primary]}' is appended to identified tokens list")
            return 1

        invalid_objects = True
        for key, value in self.game_objects_dictionary.items():
            if word in value['long']:
                self.debug(f"'{word}' is in {key}'s long name ('{key.long}')")
                value['score'] += 1
                self.debug(f"{key}'s score is increased to {value['score']}")
                invalid_objects = False
        if invalid_objects:
            # verbs_ignoring_object_validity = ['wait', 'ask', 'tell']
            # if self.verb in verbs_ignoring_object_validity:
            return 1
            # self.debug(f"No object has '{word}' in its long name")
            # return INVALID_OBJECTS

        return 1

    def parse_ambiguous(self, ambiguous_objects):
        outcome = Outcome(AMBIGUOUS_OBJECTS, self.verb, ambiguous_objects=ambiguous_objects)
        result = Result(None, outcome)
        result.show()
        input_words = input("> ")
        parser = Parser(self.world, input_words, silent=True, advance_time=False)
        parser.ambiguous_objects = ambiguous_objects
        parser.parse()
        if len(parser.identified_tokens) == 1:
            return parser.identified_tokens[0]

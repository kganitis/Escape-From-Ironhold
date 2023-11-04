from unittest import TestCase

from nlp.parser import parse
from game.game import Game
from game.outcomes import *


class TestActions(TestCase):
    def assert_result(self, *expected_results):
        expected_results = expected_results[0] if isinstance(expected_results[0], list) else [expected_results]
        commands = list(self.commands) if isinstance(self.commands, tuple) else [self.commands]
        game = Game(test=True)
        game.world.populate()
        results = []

        for cmd in commands:
            results = parse(game.world, cmd)

        self.assertEqual(len(results), len(expected_results))

        for result, expected in zip(results, expected_results):
            self.assertEqual(expected[0], (result.outcome, result.type))
            self.assertEqual(result.related_objects, expected[1])

    def test_take(self):
        self.commands = "take"
        self.assert_result(INVALID_COMMAND, [])

    def test_take_obtainable(self):
        self.commands = "take lockpick"
        self.assert_result(TAKE_SUCCESS, ["lockpick"])

    def test_take_non_obtainable(self):
        self.commands = "take lock"
        self.assert_result(NOT_OBTAINABLE, ["lock"])

    def test_take_already_obtained(self):
        self.commands = "take lockpick", "take lockpick"
        self.assert_result(ALREADY_OBTAINED, ["lockpick"])

    def test_take_out_of_scope(self):
        self.commands = "take barel"
        self.assert_result(OUT_OF_SCOPE, ["barel"])

    def test_take_nonsense(self):
        self.commands = "take nonsense"
        self.assert_result(INVALID_OBJECTS, ["nonsense"])

    def test_take_multiple(self):
        # same attributes
        self.commands = "take lock door"
        self.assert_result(NOT_OBTAINABLE, ["lock", "door"])

        # different attributes
        self.commands = "take nonsense barel lock lockpick"
        result1 = INVALID_OBJECTS, ["nonsense"]
        result2 = OUT_OF_SCOPE, ["barel"]
        result3 = NOT_OBTAINABLE, ["lock"]
        result4 = TAKE_SUCCESS, ["lockpick"]
        self.assert_result([result1, result2, result3, result4])

from game.outcomes import *


class Result:
    def __init__(self, command=None, outcome_text="", related_objects=None, outcome_type=False):
        if related_objects is None:
            related_objects = []
        self.command = command
        self.outcome = outcome_text
        self.related_objects = related_objects
        self.type = outcome_type
        self.message = ""

    def show(self):
        print(self.message)

    def __eq__(self, other):
        return self.command == other.command and self.outcome == other.create_outcome and self.type == other.type and self.message == other.message

    def __str__(self):
        return f"{self.command} => ({self.outcome}, {self.related_objects}, {self.type})"

    def is_fail_or_error(self):
        return self.type == FAIL or self.type == INVALID

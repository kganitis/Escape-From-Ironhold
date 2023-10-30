from game.outcomes import *


class Result:
    def __init__(self, command=None, outcome_text="", related_elements=None, outcome_type=False):
        if related_elements is None:
            related_elements = []
        self.command = command
        self.outcome = outcome_text
        self.related_elements = related_elements
        self.type = outcome_type
        self.message = ""

    def show(self):
        print(self.message)

    def __eq__(self, other):
        return self.command == other.command and self.outcome == other.create_outcome and self.type == other.type and self.message == other.message

    def __str__(self):
        return f"{self.command} => {self.outcome}"

    def is_fail_or_error(self):
        return self.type == FAIL or self.type == INVALID

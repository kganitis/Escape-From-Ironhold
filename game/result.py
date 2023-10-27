from game.outcomes import *


class Result:
    def __init__(self, command=""):
        self.command = command
        self.outcome = ""
        self.type = False
        self.message = ""

    def show(self):
        print(self.message)

    def __eq__(self, other):
        return self.command == other.command and self.outcome == other.outcome and self.type == other.type and self.message == other.message

    def __str__(self):
        return f"{self.command} => {self.outcome}"

    def is_fail_or_error(self):
        return self.type == FAIL or self.type == INVALID

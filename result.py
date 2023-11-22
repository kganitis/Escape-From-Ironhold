from outcomes import FAIL, INVALID


class Result:
    def __init__(self, action, outcome):
        self.action = action
        self.outcome = outcome

    def __eq__(self, other):
        return self.action == other.action and self.outcome == other.outcome

    def __str__(self):
        return f"{self.action.command} => {self.outcome}"

    def show(self):
        if self.outcome.description:
            print(self.outcome.formatted_description)

    def is_fail_or_invalid(self):
        return self.outcome.type in (FAIL, INVALID)

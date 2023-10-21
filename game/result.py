class Result:
    def __init__(self, command=""):
        self.command = command
        self.description = ""
        self.outcome = ""
        self.message = ""
        self.advance = ""

    def show(self):
        print(self.message)

    def __eq__(self, other):
        return self.command == other.command and self.description == other.description and self.outcome == other.outcome and self.message == other.message and self.advance == other.advance

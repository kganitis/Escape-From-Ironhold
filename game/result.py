class Result:
    def __init__(self, command=""):
        self.command = command
        self.description = ""
        self.outcome = ""
        self.message = ""

    def show(self):
        print(self.message)

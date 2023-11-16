from .world import World


class Game:
    def __init__(self, test=False):
        self.test = test
        self.world = World()
        self.world.populate()

    def run(self):
        print("\nWelcome to ESCAPE FROM IRONHOLD\n")

        # Print help prompt
        print("\nType 'help' to see a list of available commands.\n\n")

        # First describe the initial room
        self.world.current_room.describe()

        # Start the game loop
        while True:
            # Input
            print("\nWhat do you want to do?")
            input_command = input("> ")

            # Parse
            self.world.parse(input_command)

            # End game check
            dead_flag = self.world.player.dead_flag
            if dead_flag == 1:
                print("\n. . . GAME OVER . . .")
                break
            elif dead_flag == 2:
                print("\n! ! ! YOU WIN ! ! !")
                break

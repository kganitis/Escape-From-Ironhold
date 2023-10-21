import csv
import json

from game.game import Game


def test_run(game):
    results = game.generate_all_possible_results(3)

    # Save results to JSON file
    # with open('results.json', 'w') as json_file:
    #     json.dump([result.__dict__ for result in results], json_file, indent=4)
    #     print("Successfully created results.json in the tests package")
    #     json_file.close()
    #
    # # Save results to CSV file
    # with open('results.csv', 'w', newline='') as csv_file:
    #     writer = csv.DictWriter(csv_file, fieldnames=results[0].__dict__.keys())
    #     writer.writeheader()
    #     for result in results:
    #         writer.writerow(result.__dict__)
    #     print("Successfully created results.csv in the tests package")
    #     csv_file.close()

    save_results_to_csv(results, "results.csv")


def save_results_to_csv(results, csv_filename):
    with open(csv_filename, mode='w', newline='') as csv_file:
        fieldnames = ["command", "result"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for result in results:
            writer.writerow(result)


def main():
    # Get all possible results for every possible command
    test_run(Game())


if __name__ == "__main__":
    main()

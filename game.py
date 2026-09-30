import random
from logic import feedback


class Mastermind:
    DIFFICULTIES = {
        "easy": {
            "length": 3,
            "max_symbol": 4,
            "turns": 12,
        },
        "medium": {
            "length": 4,
            "max_symbol": 6,
            "turns": 10,
        },
        "hard": {
            "length": 5,
            "max_symbol": 8,
            "turns": 8,
        },
    }

    def __init__(self, difficulty="medium"):
        self.difficulty = difficulty.lower()

        if self.difficulty not in self.DIFFICULTIES:
            self.difficulty = "medium"

        settings = self.DIFFICULTIES[self.difficulty]

        self.code_length = settings["length"]
        self.max_symbol = settings["max_symbol"]
        self.turns = settings["turns"]

        self.code = [
            str(random.randint(1, self.max_symbol))
            for _ in range(self.code_length)
        ]

        self.history = []
        self.game_over = False
        self.won = False

    # Difficulty selection
    def choose_difficulty(self):
        print("\nChoose difficulty:")
        print("1. Easy   - 3 symbols, values 1-4, 12 turns")
        print("2. Medium - 4 symbols, values 1-6, 10 turns")
        print("3. Hard   - 5 symbols, values 1-8, 8 turns")

        choices = {
            "1": "easy",
            "2": "medium",
            "3": "hard",
        }

        while True:
            choice = input("Select difficulty (1-3): ").strip()

            if choice in choices:
                self.difficulty = choices[choice]

                settings = self.DIFFICULTIES[self.difficulty]

                self.code_length = settings["length"]
                self.max_symbol = settings["max_symbol"]
                self.turns = settings["turns"]

                self.code = [
                    str(random.randint(1, self.max_symbol))
                    for _ in range(self.code_length)
                ]

                return

            print("Invalid choice. Please select 1, 2, or 3.")

    # Input validation
    def valid_guess(self, raw):
        if len(raw) != self.code_length:
            return False

        allowed_symbols = "".join(
            str(i) for i in range(1, self.max_symbol + 1)
        )

        return all(ch in allowed_symbols for ch in raw)

    # Display previous guesses
    def display_history(self):
        if not self.history:
            return

        print("\nGuess History")
        print("-" * 45)

        for number, (guess, exact, partial) in enumerate(
            self.history, start=1
        ):
            print(
                f"{number:>2}. "
                f"{guess}  |  "
                f"Exact: {exact}  |  "
                f"Partial: {partial}"
            )

        print("-" * 45)

    # End-of-game handling
    def finish_game(self):
        if self.won:
            print("\nCracked the code!")
            print(f"You solved it in {len(self.history)} guess(es).")

        else:
            print("\nNo turns remaining.")
            print("The code was:", "".join(self.code))

        self.display_history()

    # Main game loop
    def run(self):
        if self.game_over:
            print("This game has already ended.")
            return

        self.choose_difficulty()

        print("\nMastermind")
        print(
            f"Difficulty: {self.difficulty.capitalize()}"
        )
        print(
            f"Enter {self.code_length} digits from "
            f"1 to {self.max_symbol}."
        )
        print("Enter 'q' at any time to quit.")

        while self.turns > 0 and not self.game_over:

            print(f"\n{self.turns} turns left")

            raw = input("> ").strip()

            # Quit
            if raw.lower() == "q":
                print("\nGame abandoned.")
                self.game_over = True
                self.display_history()
                return

            # Invalid input
            if not self.valid_guess(raw):
                print(
                    f"Invalid guess. Enter exactly "
                    f"{self.code_length} digits from "
                    f"1 to {self.max_symbol}."
                )

                # Important:
                # An invalid guess does NOT consume a turn.
                continue

            # Process accepted guess
            guess = list(raw)

            exact, partial = feedback(self.code, guess)

            # Only accepted guesses reach this point,
            # so only accepted guesses are added to history.
            self.history.append((raw, exact, partial))

            self.turns -= 1

            print(
                f"Exact: {exact}  |  Partial: {partial}"
            )

            # Win condition
            if exact == self.code_length:
                self.won = True
                self.game_over = True
                self.finish_game()
                return

        # Loss condition
        if not self.game_over:
            self.game_over = True
            self.finish_game()
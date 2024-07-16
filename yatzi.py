import random
from typing import Callable
from combinations import COMBINATIONS, Combination
from copy import deepcopy

RETHROWS: int = 2
DICE: int = 6

class Player:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.dice: list[int] = [0 for _ in range(DICE)]

        self.combinations: list[Combination] = deepcopy(COMBINATIONS)

        self.score_sum: Callable[[], int] = lambda: sum([
            combination.score 
            for combination in self.combinations
        ])

    def throw(self, unkept: list[int] = list(range(6))) -> None:
        self.dice = [
            random.randint(1, 6) if i in unkept else die 
            for i, die in enumerate(self.dice)
        ]

    def __roll(self) -> None:
        self.throw()
        skip: bool = False
        for i in range(RETHROWS):
            print(f"rethrows: {i}/{RETHROWS}")
            print(self)
            while True:
                unkept: list[str] = [i for i in input("Dice to throw away: ").split(" ")]
                try:
                    self.throw([int(i) for i in unkept])
                    break
                except ValueError:
                    if unkept[0] == "":
                        self.throw()
                        skip = True
                        break
                    print("Make sure to only include numbers or blank space!")
            if skip:
                break
        if not skip:
            print(self)

    def __mark(self) -> None:
        index: int = 0
        while True:
            try:
                index = int(input("What combination to mark?\nINPUT: "))
                if not self.combinations[index].marked:
                    break
                print("Already used this combination!")
            except ValueError:
                print("Bad input!")
            except IndexError:
                print("Make sure number is in range!")
        self.combinations[index].mark(self.combinations[index].check(self.dice))

    def play(self) -> None:
        self.__roll()
        self.__mark()

    def __str__(self) -> str:
        string: str = f"NAME: {self.name}"
        for i, combination in enumerate(self.combinations):
            if type(self) == Bot and not combination.marked:
                continue
            string += (
                f"\n{' ' if i < 10 else ''}{i}" + 
                f":[{'X' if combination.marked else ' '}]\t{combination.name}: " + 
                f"\tscore: {combination.score},{f'\tthrow: {combination.check(self.dice)}' if type(self) != Bot else ''}"
            )
        string += f"\n\t\t\ttotal: {self.score_sum()}\n"
        if type(self) == Bot:
            return string
        string += f"INDEX: {list(range(DICE))}\nDICE:  {self.dice}"
        return string

    def out(self) -> bool:
        for combination in self.combinations:
            if not combination.marked:
                return False
        return True

class Bot(Player):
    def __best_combination(self) -> tuple[int, int]:
        # return [index, score]
        ret: tuple[int, int] = (0, -1)
        for i, combination in enumerate(self.combinations):
            if combination.check(self.dice) > ret[1] and not combination.marked:
                ret = (i, combination.check(self.dice))
        return ret

    def __roll(self) -> None:
        print(f"{self.name}:")
        self.throw()
        for _ in range(RETHROWS):
            best: tuple[int, int] = self.__best_combination()
            print(f"DICE: {self.dice}")
            print(f"{self.name}'s best is '{self.combinations[best[0]].name}' score: {best[1]}")

            bad_dice: list[int] = [
                i
                for i in range(DICE)
                if self.combinations[best[0]].check([
                    die for j, die in enumerate(self.dice) if j != i
                ]) >= best[1]
            ]
            print(f"bad_dice: {bad_dice}")
            if len(bad_dice) == 0:
                break

            self.throw(bad_dice)
        print(f"DICE: {self.dice}")
        best: tuple[int, int] = self.__best_combination()
        print(f"{self.name} marks '{self.combinations[best[0]].name}' and scores: {best[1]}")

    def __mark(self) -> None:
        index: int = self.__best_combination()[0]
        self.combinations[index].mark(self.combinations[index].check(self.dice))
        print(self)

    def play(self) -> None:
        self.__roll()
        self.__mark()

class YatzyGame:
    def __init__(self) -> None:
        player_names: str = input("Give player names, seperated by spaces: ")
        players: list[str] = []
        if player_names != "":
             players = player_names.split(" ")

        bot_count: int = int(input("Number of bots: "))
        self.players: list[Player] = (
            [Player(name) for name in players] + 
            [Bot(f"Bot: {i}") for i in range(bot_count)]
        )
        random.shuffle(self.players)

    def run(self) -> None:
        for _ in range(len(COMBINATIONS)):
            for player in self.players:
                player.play()
                print("-" * 50)

        winner: Player = sorted(self.players, key=lambda player: player.score_sum(), reverse=True)[0]
        print(f"Game ended!\nThe winner is: {winner}")

if __name__ == "__main__":
    YatzyGame().run()

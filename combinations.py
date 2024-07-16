class Combination:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.simple: bool = False
        self.marked: bool = False
        self.score: int = 0

    # returns 0 if not correct
    def check(self, dice: list[int]) -> int:
        return sum(dice)

    def mark(self, score: int) -> None:
        if self.marked:
            return
        self.score = score
        self.marked = True

class Simple_num(Combination):
    def __init__(self, num: int) -> None:
        super().__init__(f"Sum {num}'s")
        self.simple = True
        self.num: int = num

    def check(self, dice: list[int]) -> int:
        return sum([die for die in dice if die == self.num])

class Pairs(Combination):
    def __init__(self, count: int) -> None:
        super().__init__(f"{count} pair{'s' if count > 1 else ''}")
        self.count = count

    def check(self, dice: list[int]) -> int:
        pair_scores: list[int] = []
        for i in range(1, 7):
            count: int = dice.count(i)
            if count >= 2:
                pair_scores.append(i * 2)

        if len(pair_scores) < self.count:
            return 0
        return sum([pair_scores[len(pair_scores) - i - 1] for i in range(self.count)])

class Alike(Combination):
    def __init__(self, count: int) -> None:
        super().__init__(f"{count} alike")
        self.count: int = count

    def check(self, dice: list[int]) -> int:
        for i in range(6, 0, -1):
            count: int = dice.count(i)
            if count >= self.count:
                return self.count * i
        return 0

class Straight(Combination):
    def __init__(self, name: str = "full", nums: list[int] = list(range(1, 7))) -> None:
        super().__init__(f"{name} straight")
        self.nums: list[int] = nums

    def check(self, dice: list[int]) -> int:
        if self.nums == sorted(dice):
            return sum(dice)
        return 0

class House(Combination):
    # make sure the bigger count is first
    def __init__(self, name: str = "small", counts: list[int] = [3, 2]) -> None:
        super().__init__(f"{name} house")
        self.counts: list[int] = counts

    def check(self, dice: list[int]) -> int:
        nums: list[int] = []
        for count in self.counts:
            skip: bool = False
            for i in range(6, 0, -1):
                if i in nums:
                    continue
                if dice.count(i) >= count:
                    nums.append(i)
                    skip = True
                if skip:
                    break
            if skip:
                continue
        if len(nums) >= 2:
            return sum([num * self.counts[i] for i, num in enumerate(nums)])
        return 0 

class Yatzi(Combination):
    def __init__(self) -> None:
        super().__init__("maxi YATZI")

    def check(self, dice: list[int]) -> int:
        for i in range(6, 0, -1):
            if len(dice) == dice.count(i):
                return 100
        return 0

# needs to be deepcopied for each player (efficiency, ikr :)
COMBINATIONS: list[Combination] = [
    Simple_num(i) for i in range(1, 7)] + [
    Pairs(i) for i in range(1, 4)] + [
    Alike(i) for i in range(3, 6)] + [
    Straight(), Straight("low", list(range(1, 6))), Straight("high", list(range(2, 7)))] + [
    House(), House("big", [3, 3]), House("tower", [4, 2])] + [
    Combination("chance"), Yatzi()
]

def __test() -> None:
    dice: list[int] = [2, 2, 2, 2, 2, 2]
    print("dice: ", dice)
    for i in COMBINATIONS:
        print(f"{i.name}: {i.check(dice)}")

if __name__ == "__main__":
    __test()

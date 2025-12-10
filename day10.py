import re
from itertools import combinations
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, milp

type Machine = tuple[set[int], list[set[int]], list[int]]


def read_input(path: Path) -> list[Machine]:
    machines: list[Machine] = []
    for line in path.read_text().splitlines():
        target_match = re.search(r"\[([.#]+)\]", line)
        assert target_match
        lights = {i for i, c in enumerate(target_match.group(1)) if c == "#"}

        buttons: list[set[int]] = []
        for button_match in re.finditer(r"\(([0-9,]+)\)", line):
            buttons.append({int(x) for x in button_match.group(1).split(",")})

        joltage_match = re.search(r"\{([0-9,]+)\}", line)
        assert joltage_match
        joltage = [int(x) for x in joltage_match.group(1).split(",")]

        machines.append((lights, buttons, joltage))
    return machines


def min_presses_xor(target: set[int], buttons: list[set[int]]) -> int:
    n = len(buttons)
    for k in range(n + 1):
        for combo in combinations(range(n), k):
            result = set[int]()
            for i in combo:
                result ^= buttons[i]
            if result == target:
                return k
    raise ValueError("No solution found")


def min_presses_sum(buttons: list[set[int]], targets: list[int]) -> int:
    n_buttons = len(buttons)
    n_counters = len(targets)

    A = np.zeros((n_counters, n_buttons))
    for i, button in enumerate(buttons):
        for j in button:
            A[j, i] = 1

    result = milp(
        c=np.ones(n_buttons),
        integrality=np.ones(n_buttons),
        bounds=Bounds(lb=0, ub=np.inf),
        constraints=(A, targets, targets),
    )
    return int(round(result.fun))


def part1(machines: list[Machine]) -> int:
    return sum(min_presses_xor(lights, buttons) for lights, buttons, _ in machines)


def part2(machines: list[Machine]) -> int:
    return sum(min_presses_sum(buttons, joltage) for _, buttons, joltage in machines)


if __name__ == "__main__":
    data = read_input(Path("./day10.txt"))
    print("part 1:", part1(data))
    print("part 2:", part2(data))

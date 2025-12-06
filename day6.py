import operator
from functools import reduce
from pathlib import Path


def read_input(path: Path) -> list[list[str]]:
    data = path.read_text().splitlines()
    lines = data[:-1]
    op_line = data[-1]
    max_len = max(len(line) for line in lines)

    separators: list[int] = []
    for pos in range(max_len):
        if all(pos < len(line) and line[pos] == " " for line in lines):
            separators.append(pos)

    boundaries: list[int] = []
    i = 0
    while i < len(separators):
        j = i
        while j < len(separators) - 1 and separators[j + 1] == separators[j] + 1:
            j += 1
        boundaries.append(separators[i])
        i = j + 1

    columns: list[list[str]] = []
    start = 0
    for boundary in boundaries:
        column = [line[start:boundary] for line in lines]
        column.append(op_line[start:boundary])
        columns.append(column)
        start = boundary + 1

    column = [line[start:] for line in lines]
    column.append(op_line[start:])
    columns.append(column)

    return columns


def part1(data: list[list[str]]) -> int:
    total = 0
    for line in data:
        op = line[-1].strip()
        nums = map(int, line[:-1])
        if op == "+":
            total += sum(nums)
        else:  # op == "*"
            total += reduce(operator.mul, nums)
    return total


def part2(data: list[list[str]]) -> int:
    total = 0
    for line in data:
        op = line[-1].strip()
        nums = line[:-1]
        digits = map(list, nums)
        digits = list(zip(*digits))
        nums = [int("".join(ds)) for ds in digits]
        if op == "+":
            total += sum(nums)
        else:  # op == "*"
            total += reduce(operator.mul, nums)
    return total


if __name__ == "__main__":
    data = read_input(Path("./day6.txt"))
    print("part 1:", part1(data))
    print("part 2:", part2(data))

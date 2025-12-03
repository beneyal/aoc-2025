from pathlib import Path


def read_input(path: Path) -> list[list[int]]:
    data = path.read_text().splitlines()
    data = [list(map(int, list(line))) for line in data]
    return data


def _run(data: list[list[int]], n: int) -> int:
    total = 0
    for line in data:
        digits: list[int] = []
        start = 0
        for i in range(n):
            end = len(line) - (n - i) + 1
            biggest_idx = max(range(start, end), key=line.__getitem__)
            digits.append(line[biggest_idx])
            start = biggest_idx + 1
        total += int("".join(map(str, digits)))
    return total


def part1(data: list[list[int]]) -> int:
    return _run(data, 2)


def part2(data: list[list[int]]) -> int:
    return _run(data, 12)


if __name__ == "__main__":
    data = read_input(Path("./day3.txt"))
    print("part 1:", part1(data))
    print("part 2:", part2(data))

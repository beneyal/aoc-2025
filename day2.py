from pathlib import Path
import re


def read_input(path: Path) -> list[range]:
    data = path.read_text()
    ranges = [s.split("-") for s in data.split(",")]
    ranges = [range(int(a), int(b) + 1) for a, b in ranges]
    return ranges


def part1(ranges: list[range]) -> int:
    total = 0
    for rng in ranges:
        for n in map(str, rng):
            if re.fullmatch(r"(\d+)\1", n):
                total += int(n)
    return total


def part2(ranges: list[range]) -> int:
    total = 0
    for rng in ranges:
        for n in map(str, rng):
            for length in range(len(n), 0, -1):
                pat = re.compile(rf"(\d+){r'\1' * length}")
                if pat.fullmatch(n):
                    total += int(n)
                    break
    return total


if __name__ == "__main__":
    ranges = read_input(Path("./day2.txt"))
    print("part 1:", part1(ranges))
    print("part 2:", part2(ranges))

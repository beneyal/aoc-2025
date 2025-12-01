from pathlib import Path


def part1(inp: list[str]) -> int:
    times = 0
    safe = 50
    for d, n in [(s[0], int(s[1:])) for s in inp]:
        if d == "R":
            safe += n
        else:  # d == "L"
            safe -= n
        safe %= 100
        times += safe == 0
    return times


def part2(inp: list[str]) -> int:
    times = 0
    safe = 50
    for d, n in [(s[0], int(s[1:])) for s in inp]:
        for _ in range(n):
            if d == "R":
                safe += 1
            else:  # d == "L"
                safe -= 1
            safe %= 100
            times += safe == 0
    return times


if __name__ == "__main__":
    inp = Path("day1.txt").read_text().splitlines()

    print(part1(inp))
    print(part2(inp))

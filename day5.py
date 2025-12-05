from pathlib import Path


def read_input(path: Path) -> tuple[list[range], list[int]]:
    data = path.read_text()
    fresh, available = data.split("\n\n")
    fresh = [range(int(a), int(b) + 1) for a, b in map(lambda s: s.split("-"), fresh.split("\n"))]
    available = [int(x) for x in available.split("\n")]
    return fresh, available


def part1(fresh: list[range], available: list[int]) -> int:
    total = 0
    for a in available:
        for f in fresh:
            if a in f:
                total += 1
                break
    return total


def part2(fresh: list[range]) -> int:
    intervals = sorted([(r.start, r.stop) for r in fresh])

    merged = [intervals[0]]

    for start, stop in intervals[1:]:
        last_start, last_stop = merged[-1]

        if start <= last_stop:
            merged[-1] = (last_start, max(last_stop, stop))
        else:
            merged.append((start, stop))

    return sum(stop - start for start, stop in merged)


if __name__ == "__main__":
    fresh, available = read_input(Path("./day5.txt"))
    print("part 1:", part1(fresh, available))
    print("part 2:", part2(fresh))

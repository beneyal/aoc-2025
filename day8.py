from collections.abc import Iterator
from itertools import combinations
from math import hypot
from pathlib import Path

type Point = tuple[int, int, int]


def _euclidean_distance(p1: Point, p2: Point) -> float:
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return hypot(x2 - x1, y2 - y1, z2 - z1)


def _merge_circuits(points: list[Point], limit: int | None = None) -> Iterator[tuple[Point, Point, list[set[Point]]]]:
    point_pairs = sorted(combinations(points, 2), key=lambda pair: _euclidean_distance(*pair))
    circuits: list[set[Point]] = []

    for p1, p2 in point_pairs[:limit]:
        c1: set[Point] | None = None
        c2: set[Point] | None = None
        for c in circuits:
            if p1 in c:
                c1 = c
            if p2 in c:
                c2 = c

        if c1 is None and c2 is None:
            circuits.append({p1, p2})
        elif c1 is None and c2 is not None:
            c2.add(p1)
        elif c2 is None and c1 is not None:
            c1.add(p2)
        elif c1 is not None and c2 is not None and c1 is not c2:
            c1.update(c2)
            circuits.remove(c2)

        yield p1, p2, circuits


def read_input(path: Path) -> list[Point]:
    data = path.read_text().splitlines()
    return [(x, y, z) for x, y, z in map(lambda s: map(int, s.split(",")), data)]


def part1(points: list[Point], to_consider: int) -> int:
    *_, (_, _, circuits) = _merge_circuits(points, to_consider)
    sizes = sorted(map(len, circuits), reverse=True)
    return sizes[0] * sizes[1] * sizes[2]


def part2(points: list[Point]) -> int:
    for p1, p2, circuits in _merge_circuits(points):
        if len(circuits) == 1 and len(circuits[0]) == len(points):
            return p1[0] * p2[0]
    raise AssertionError("This will never happen, right?")


if __name__ == "__main__":
    data = read_input(Path("./day8.txt"))
    print("part 1:", part1(data, 1000))
    print("part 2:", part2(data))

from collections import deque
from functools import cache
from pathlib import Path

type Node = tuple[int, int]
type Grid = list[list[str]]


def read_input(path: Path) -> tuple[Grid, Node]:
    data = [list(line) for line in path.read_text().splitlines()]
    src: Node = (0, data[0].index("S"))
    return data, src


def part1(grid: Grid, src: Node) -> int:
    splits = 0
    i, j = src
    beams = deque[Node]([(i + 1, j)])
    seen = set[Node]()
    while len(beams) > 0:
        node = beams.popleft()
        if node in seen:
            continue
        seen.add(node)
        i, j = node
        if i >= len(grid):
            break
        if grid[i][j] == "^":
            splits += 1
            beams.extend([(i + 1, j - 1), (i + 1, j + 1)])
        else:  # grid[i][j] == "."
            beams.append((i + 1, j))
    return splits


def part2(grid: Grid, src: Node) -> int:
    @cache
    def count_paths(i: int, j: int) -> int:
        while i < len(grid):
            if grid[i][j] == "^":
                return count_paths(i + 1, j - 1) + count_paths(i + 1, j + 1)
            i += 1
        return 1

    i, j = src
    return count_paths(i + 1, j)


if __name__ == "__main__":
    grid, src = read_input(Path("./day7.txt"))
    print("part 1:", part1(grid, src))
    print("part 2:", part2(grid, src))

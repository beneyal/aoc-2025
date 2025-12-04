from pathlib import Path


def read_input(path: Path) -> list[list[str]]:
    data = path.read_text().splitlines()
    data = [list(line) for line in data]
    return data


def _get_positions_to_rolls_counts(grid: list[list[str]]) -> dict[tuple[int, int], int]:
    d: dict[tuple[int, int], int] = {}
    for i, line in enumerate(grid):
        for j in range(len(line)):
            if grid[i][j] != "@":
                continue
            rolls = 0
            for di, dj in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                if 0 <= i + di < len(grid) and 0 <= j + dj < len(line) and grid[i + di][j + dj] == "@":
                    rolls += 1
            d[i, j] = rolls
    return d


def _mutate_grid(grid: list[list[str]], ps: set[tuple[int, int]]) -> None:
    for i, line in enumerate(grid):
        for j in range(len(line)):
            if (i, j) in ps:
                grid[i][j] = "."


def part1(grid: list[list[str]]) -> int:
    return sum(1 for v in _get_positions_to_rolls_counts(grid).values() if v < 4)


def part2(grid: list[list[str]]) -> int:
    total = 0
    d = _get_positions_to_rolls_counts(grid)
    while (rolls := sum(1 for v in d.values() if v < 4)) > 0:
        total += rolls
        remove = set([k for k, v in d.items() if v < 4])
        _mutate_grid(grid, remove)
        d = _get_positions_to_rolls_counts(grid)
    return total


if __name__ == "__main__":
    grid = read_input(Path("./day4.txt"))
    print("part 1:", part1(grid))
    print("part 2:", part2(grid))

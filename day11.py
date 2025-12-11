from collections import defaultdict
from functools import cache
from pathlib import Path

type Graph = defaultdict[str, set[str]]


def read_input(path: Path) -> Graph:
    g: defaultdict[str, set[str]] = defaultdict(set)
    for line in path.read_text().splitlines():
        src, dsts = line.split(": ", maxsplit=1)
        dsts = dsts.split(" ")
        g[src] = set(dsts)
    return g


def part1(g: Graph) -> int:
    stack = ["you"]
    outs = 0
    while len(stack) > 0:
        src = stack.pop()
        if src == "out":
            outs += 1
        dsts = g[src]
        stack.extend(dsts)
    return outs


def part2(g: Graph) -> int:
    @cache
    def count_paths(node: str, seen_dac: bool, seen_fft: bool) -> int:
        seen_dac = seen_dac or node == "dac"
        seen_fft = seen_fft or node == "fft"

        if node == "out":
            return 1 if (seen_dac and seen_fft) else 0

        total = 0
        for dst in g[node]:
            total += count_paths(dst, seen_dac, seen_fft)
        return total

    return count_paths("svr", False, False)


if __name__ == "__main__":
    g = read_input(Path("./day11.txt"))
    print("part 1:", part1(g))
    print("part 2:", part2(g))

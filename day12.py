from pathlib import Path

type Region = tuple[int, int, list[int]]


def read_input(path: Path) -> tuple[list[int], list[Region]]:
    data = path.read_text()
    parts = data.split("\n\n")
    cell_counts = [part.count("#") for part in parts[:-1]]
    regions: list[Region] = []
    for line in parts[-1].split("\n"):
        dims, counts_str = line.split(": ")
        w, h = map(int, dims.split("x"))
        counts = list(map(int, counts_str.split()))
        regions.append((w, h, counts))
    return cell_counts, regions


def part1(cell_counts: list[int], regions: list[Region]) -> int:
    count = 0
    for width, height, counts in regions:
        total_needed = sum(c * cc for c, cc in zip(counts, cell_counts))
        if total_needed <= width * height:
            count += 1
    return count


if __name__ == "__main__":
    cell_counts, regions = read_input(Path("./day12.txt"))
    print("part 1:", part1(cell_counts, regions))

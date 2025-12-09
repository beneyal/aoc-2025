from itertools import combinations
from pathlib import Path
from typing import NamedTuple

type Point = tuple[int, int]


class VerticalEdge(NamedTuple):
    x: int
    y1: int
    y2: int
    lo: int
    hi: int


class HorizontalEdge(NamedTuple):
    y: int
    lo: int
    hi: int


def _area(p1: Point, p2: Point) -> int:
    x1, y1 = p1
    x2, y2 = p2
    return (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)


def _precompute_edges(polygon: list[Point]) -> tuple[list[VerticalEdge], list[HorizontalEdge]]:
    vertical = []
    horizontal = []
    for i in range(len(polygon)):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % len(polygon)]
        if x1 == x2:
            vertical.append(VerticalEdge(x=x1, y1=y1, y2=y2, lo=min(y1, y2), hi=max(y1, y2)))
        else:
            horizontal.append(HorizontalEdge(y=y1, lo=min(x1, x2), hi=max(x1, x2)))
    return vertical, horizontal


def _point_in_polygon(
    point: Point,
    vertical_edges: list[VerticalEdge],
    horizontal_edges: list[HorizontalEdge],
    vertices: set[Point],
) -> bool:
    if point in vertices:
        return True

    x, y = point
    crossings = 0

    for edge in vertical_edges:
        if x == edge.x and edge.lo <= y <= edge.hi:
            return True
        edge_crosses_ray_height = (edge.y1 > y) != (edge.y2 > y)
        edge_is_to_the_right = x < edge.x
        if edge_crosses_ray_height and edge_is_to_the_right:
            crossings += 1

    for edge in horizontal_edges:
        if y == edge.y and edge.lo <= x <= edge.hi:
            return True

    return crossings % 2 == 1


def _rect_in_polygon(
    p1: Point,
    p2: Point,
    vertical_edges: list[VerticalEdge],
    horizontal_edges: list[HorizontalEdge],
    vertices: set[Point],
) -> bool:
    rx1, rx2 = min(p1[0], p2[0]), max(p1[0], p2[0])
    ry1, ry2 = min(p1[1], p2[1]), max(p1[1], p2[1])

    corners = [(rx1, ry1), (rx1, ry2), (rx2, ry1), (rx2, ry2)]
    if not all(_point_in_polygon(c, vertical_edges, horizontal_edges, vertices) for c in corners):
        return False

    for edge in vertical_edges:
        edge_x_inside_rect = rx1 < edge.x < rx2
        edge_overlaps_rect_y = edge.lo < ry2 and edge.hi > ry1
        if edge_x_inside_rect and edge_overlaps_rect_y:
            return False

    for edge in horizontal_edges:
        edge_y_inside_rect = ry1 < edge.y < ry2
        edge_overlaps_rect_x = edge.lo < rx2 and edge.hi > rx1
        if edge_y_inside_rect and edge_overlaps_rect_x:
            return False

    return True


def read_input(path: Path) -> list[Point]:
    return [(int(a), int(b)) for a, b in (line.split(",") for line in path.read_text().splitlines())]


def part1(points: list[Point]) -> int:
    return max((abs(x2 - x1) + 1) * (abs(y2 - y1) + 1) for (x1, y1), (x2, y2) in combinations(points, 2))


def part2(points: list[Point]) -> int:
    vertical_edges, horizontal_edges = _precompute_edges(points)
    vertices = set(points)
    pairs = sorted(combinations(points, 2), key=lambda p: _area(*p), reverse=True)
    for p1, p2 in pairs:
        if _rect_in_polygon(p1, p2, vertical_edges, horizontal_edges, vertices):
            return _area(p1, p2)
    raise AssertionError("This will never happen...")


if __name__ == "__main__":
    data = read_input(Path("./day9.txt"))
    print("part 1:", part1(data))
    print("part 2:", part2(data))

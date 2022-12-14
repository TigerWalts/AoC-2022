from copy import deepcopy
from io import TextIOWrapper
from os import path
from typing import Dict, Generator, Iterable, List, Set, Tuple

Vec2D = Tuple[int,int]

FOLDER = path.dirname(__file__)
INPUT = path.join(FOLDER, 'input.txt')

CHECKS: List[Vec2D] = [
    (0, 1),
    (-1, 1),
    (1, 1)
]

def add_vectors(iter: Iterable[Vec2D])-> Vec2D:
    return tuple(map(sum, zip(*iter)))

def iter_line(file_object: TextIOWrapper):
    for line in file_object:
        yield line.strip()

def iter_coords(line: str) -> Generator[Vec2D, None, None]:
    for coord_str in line.split(' -> '):
        yield tuple(map(int, coord_str.split(',')))

def iter_pairwise_coords(iter: Iterable[Vec2D]) -> Generator[Tuple[Vec2D,Vec2D], None, None]:
    last = next(iter)
    for item in iter:
        yield last, item
        last = item

def iter_rocks_from_coord_pairs(iter: Iterable[Tuple[Vec2D,Vec2D]]):
    for first, last in iter:
        xs, ys = tuple(map(lambda x : range(x[0], x[1]+1),map(sorted,zip(first,last))))
        for x in xs:
            for y in ys:
                yield x, y

def print_grid(grid: Dict[Vec2D,str], xs: Iterable[int], ys: Iterable[int]):
    for y in ys:
        print(''.join(grid[(x, y)] for x in xs))

def simulate(grid):
    grain = (500, 0)
    while grain is not None:
        test_locs = [ add_vectors((grain, check)) for check in CHECKS if add_vectors((grain, check)) in grid.keys() ]
        test_vals = [ grid[test_loc] for test_loc in test_locs ]
        if '.' in test_vals:
            grain = test_locs[test_vals.index('.')]
            continue
        if len(test_vals) == 3:
            grid[grain] = 'O'
            grain = (500, 0)
            if grid[grain] == 'O':
                grain = None
            continue
        grain = None

def main():
    # Get rocks
    rocks: Set[Vec2D] = set()
    with open(INPUT, 'r') as input_file:
        for line in iter_line(input_file):
            for rock in iter_rocks_from_coord_pairs(
                iter_pairwise_coords(iter_coords(line))
            ):
                rocks.add(rock)

    # Build grid
    (min_x, max_x), (_, max_y) = tuple((min(dim), max(dim)) for dim in zip(*rocks))
    min_y = 0
    max_y += 2
    min_x, max_x = 500 - max_y, 500 + max_y
    grid = {
        (x, y): '#' if (x, y) in rocks else '.'
        for x in range(min_x, max_x +1)
        for y in range(min_y, max_y +1)
    }
    # print_grid(grid, range(min_x, max_x+1), range(min_y, max_y+1))

    grid2 = deepcopy(grid)

    simulate(grid)
    # print_grid(grid, range(min_x, max_x+1), range(0, max_y+1))
    print(sum(1 for value in grid.values() if value == 'O'))

    for x in range(min_x, max_x+1):
        grid2[(x,max_y)] = '#'
    simulate(grid2)
    # print_grid(grid2, range(min_x, max_x+1), range(0, max_y+1))
    print(sum(1 for value in grid2.values() if value == 'O'))

if __name__ == '__main__':
    main()
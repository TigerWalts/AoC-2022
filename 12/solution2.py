from enum import Enum
from io import TextIOWrapper
from os import path
from typing import Callable, Dict, Generator, Iterable, List, Tuple

FOLDER = path.dirname(__file__)
INPUT = path.join(FOLDER, 'input.txt')
HEIGHTS = 'abcdefghijklmnopqrstuvwxyz'
HEIGHTSR = list(reversed(HEIGHTS))

Vec2D = Tuple[int,int]
Cell = Dict[str,int|str]
Maze = Dict[Vec2D, Cell]

class Dir(Enum):
    U = 2**0
    D = 2**1
    L = 2**2
    R = 2**3

DIR_VECTORS: Dict[Dir, Vec2D] = {
    Dir.U: (0,-1),
    Dir.D: (0,1),
    Dir.L: (-1,0),
    Dir.R: (1,0)
}

def iter_line(file_object: TextIOWrapper) -> Generator[str, None, None]:
    for line in file_object:
        yield line.strip()

def iter_loc_char(file_object: TextIOWrapper) -> Generator[Tuple[Vec2D,str], None, None]:
    for y, line in enumerate(iter_line(file_object)):
        for x, char in enumerate(line):
            yield (x, y), char

def parse_file() -> Dict[Vec2D, str]:
    with open(INPUT, 'r') as input_file:
        return { loc: char for loc, char in iter_loc_char(input_file) }

def add_vectors(iter: Iterable[Vec2D])-> Vec2D:
    return tuple(map(sum, zip(*iter)))

def extract_start_end(char_cells: Dict[Vec2D, str]) -> Tuple[Vec2D,Vec2D]:
    ends = { char: loc for loc, char in char_cells.items() if char in 'SE' }
    start, end = ends['S'], ends['E']
    char_cells[start] = 'a'
    char_cells[end] = 'z'
    return start, end

def iter_from_directions(coll: Maze|Dict[Vec2D, str], loc: Vec2D) -> Generator[Tuple[Dir,Vec2D,Cell|str], None, None]:
    for dir in [Dir.U,Dir.D,Dir.L,Dir.R]:
        dloc = add_vectors((loc, DIR_VECTORS[dir]))
        try:
            yield dir, dloc, coll[dloc]
        except KeyError:
            pass

def get_directions(char_cells: Dict[Vec2D, str], loc: Vec2D, reverse=False) -> int:
    lookup = HEIGHTSR if reverse else HEIGHTS
    frm = lookup.index(char_cells[loc])
    return sum(
        dir.value
        for dir, _, char
        in iter_from_directions(char_cells, loc)
        if lookup.index(char) - frm < 2
    )

def update_neighbours(maze: Maze, loc: Vec2D):
    directions = maze[loc]['directions']
    for dir, tloc, cell in iter_from_directions(maze, loc):
        if dir.value & directions == 0:
            continue
        if cell['flood'] == -1:
            increment_cell(maze, tloc)

def build_maze(char_cells: Dict[Vec2D, str], reverse=False) -> Maze:
    return {
        loc: {
            'char': char,
            'directions': get_directions(char_cells, loc, reverse),
            'flood': -1 
        }
        for loc, char in char_cells.items()
    }

def increment_cell(maze: Maze, loc: Vec2D):
    maze[loc]['flood'] += 1

def solve(maze: Maze, start: Vec2D, win: Callable[[Maze],bool]):
    increment_cell(maze, start)
    while not win(maze):
        for loc, cell in maze.items():
            if cell['flood'] > -1:
                increment_cell(maze, loc)
        for loc, cell in maze.items():
            if cell['flood'] == 1:
                update_neighbours(maze, loc)
    print(maze[start]['flood'])

if __name__ == '__main__':
    char_cells = parse_file()
    start, end = extract_start_end(char_cells)
    maze1 = build_maze(char_cells)
    solve(maze1, start, lambda m : m[end]['flood'] > -1)
    maze2 = build_maze(char_cells, reverse=True)
    solve(
        maze2,
        end,
        lambda m : sum(1 for c in m.values() if c['char'] == 'a' and c['flood'] > -1) > 0
    )

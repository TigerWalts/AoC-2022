from copy import deepcopy
from enum import Enum, auto
from io import TextIOWrapper
from os import makedirs, path
from typing import Iterable, List, Tuple

FOLDER = path.dirname(__file__)
DATAFOLDER = path.join(FOLDER, 'data')
INPUT = path.join(FOLDER, 'input.txt')
WORK1 = path.join(DATAFOLDER, 'working1.txt')
WORK2 = path.join(DATAFOLDER, 'working2.txt')
DEBUG = path.join(DATAFOLDER, 'debug.txt')

HEIGHTS = 'abcdefghijklmnopqrstuvwxyz'

Vec2D = Tuple[int, int]
Maze = List[List[List[int]]]

class Dir(Enum):
    U = 2**0
    D = 2**1
    L = 2**2
    R = 2**3

DIR_VECTORS = {
    Dir.U: (0,-1),
    Dir.D: (0,1),
    Dir.L: (-1,0),
    Dir.R: (1,0)
}

def add_vectors(iter: Iterable[Vec2D])-> Vec2D:
    return tuple(map(sum, zip(*iter)))

def iter_line(file_object: TextIOWrapper):
    for line in file_object:
        yield line.strip()

def iter_column(file_object: TextIOWrapper, column_index: int):
    file_object.seek(0)
    for line in iter_line(file_object):
        yield line[column_index]

def iter_column_pairs(file_object: TextIOWrapper, column_index: int):
    file_object.seek(0)
    for line in iter_line(file_object):
        yield line[column_index]+line[column_index+1]

def can_move(frm: str, to: str) -> Tuple[bool, bool]:
    if '_' in [frm, to]:
        return False, False
    return (HEIGHTS.index(to) - HEIGHTS.index(frm) < 2, HEIGHTS.index(frm) - HEIGHTS.index(to) < 2)

def dir_to_chr(dir: int):
    return chr(dir + 65)

def chr_to_dir(char: str):
    return ord(char[0]) - 65

def get_cell(loc: Vec2D, maze: Maze) -> List[int]:
    return maze[loc[1]][loc[0]]

def increment_cell(loc: Vec2D, maze: Maze) -> None:
    maze[loc[1]][loc[0]][1] += 1

def iter_unvisited_neighbour_locs(loc: Vec2D, maze: Maze, direction: int = 0):
    dirs = get_cell(loc, maze)[0][direction]
    for dir in [Dir.U,Dir.D,Dir.L,Dir.R]:
        if dir.value & dirs == 0:
            continue
        test_loc = add_vectors((loc, DIR_VECTORS[dir]))
        if get_cell(test_loc, maze)[1] == -1:
            yield test_loc

def iter_maze(maze):
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            yield (x, y), cell

def build_maze():
    makedirs(DATAFOLDER, exist_ok=True)
    start = None
    end = None
    max_x = 0
    max_y = 0
    all_as = []
    with open(INPUT, 'r') as input_file, open(WORK1, 'w') as work1_file:
        for y, line in enumerate(iter_line(input_file)):
            max_y = y
            if y > 0:
                work1_file.write('\n')
            chars = ['_']
            for x, char in enumerate(line):
                max_x = x
                if char == 'S':
                    start = (x, y)
                    char = 'a'
                if char == 'E':
                    end = (x, y)
                    char = 'z'
                if char == 'a':
                    all_as.append((x,y))
                chars.append(char)
                if len(chars) < 3:
                    continue
                directions = tuple(map(lambda x : Dir.L.value if x else 0, can_move(chars[1], chars[0])))
                directions = add_vectors((directions, tuple(map(lambda x : Dir.R.value if x else 0, can_move(chars[1], chars[2])))))
                work1_file.write(''.join(map(dir_to_chr,directions)))
                chars = chars[1:]
            directions = tuple(map(lambda x : Dir.L.value if x else 0, can_move(chars[1], chars[0])))
            work1_file.write(''.join(map(dir_to_chr,directions)))
    with open(INPUT, 'r') as input_file, open(WORK1, 'r') as work1_file, open(WORK2, 'w') as work2_file:
        for x in range(max_x + 1):
            if x > 0:
                work2_file.write('\n')
            chars = ['_']
            dirs = [0]
            for char, dirchr in zip(iter_column(input_file, x), iter_column_pairs(work1_file, x*2)):
                if char == 'S':
                    char = 'a'
                if char == 'E':
                    char = 'z'
                chars.append(char)
                dirs.append(tuple(map(chr_to_dir,dirchr)))
                if len(chars) < 3:
                    continue
                directions = add_vectors((dirs[-2], tuple(map(lambda x : Dir.U.value if x else 0, can_move(chars[1], chars[0])))))
                directions = add_vectors((directions, tuple(map(lambda x : Dir.D.value if x else 0, can_move(chars[1], chars[2])))))
                work2_file.write(''.join(map(dir_to_chr,directions)))
                chars = chars[1:]
                dirs = dirs[1:]
            directions = add_vectors((dirs[1], tuple(map(lambda x : Dir.U.value if x else 0, can_move(chars[1], chars[0])))))
            work2_file.write(''.join(map(dir_to_chr,directions)))
    with open(WORK2, 'r') as work2_file:
        maze = [ list( map(lambda x : [tuple(map(chr_to_dir,x)), -1], iter_column_pairs(work2_file, y*2))) for y in range(max_y + 1) ]
    return maze, start, end, all_as

def main(maze, start, break_on, direction = 0):
    increment_cell(start, maze)
    while not break_on(maze):
        for loc, cell in iter_maze(maze):
            if cell[1] > -1:
                increment_cell(loc, maze)
        for loc, cell in iter_maze(maze):
            if cell[1] == 1:
                for uloc in iter_unvisited_neighbour_locs(loc, maze, direction):
                    increment_cell(uloc, maze)
    print(get_cell(start, maze)[1])

if __name__ == '__main__':
    maze1, start, end, all_as = build_maze()
    maze2 = deepcopy(maze1)
    main(maze1, start, lambda m : get_cell(end, m)[1] > -1)
    main(maze2, end, lambda m : sum(1 for loc in all_as if get_cell(loc, m)[1] > -1) > 0, 1)
from io import TextIOWrapper
from os import path
from typing import Dict, Iterable, Set, Tuple

FOLDER = path.dirname(__file__)
INPUT = path.join(FOLDER, 'input.txt')

Vector = Tuple[int, int]

directions: Dict[str, Vector] = {
    'U': (0, 1),
    'D': (0, -1),
    'L': (-1, 0),
    'R': (1, 0)
}

def line_iter(file_object: TextIOWrapper):
    for line in file_object:
        yield line.strip()

def add_vectors(iter: Iterable[Vector])-> Vector:
    return tuple(map(sum, zip(*iter)))

def distances(vec1: Vector, vec2: Vector) -> Vector:
    return tuple(map(lambda x : x[0] - x[1], zip(vec1, vec2)))

def normalize(vec: Vector) -> Vector:
    return tuple(map(lambda x : 0 if x == 0 else (1 if x > 0 else -1), vec))

def main(size: int):
    if size < 2:
        raise ValueError('size must be 2 or greater')
    start: Vector = (0,0)
    snake = [ start for _ in range(size) ]
    visited: Set[Vector] = {snake[-1]}
    with open(INPUT, 'r') as input_file:
        for line in line_iter(input_file):
            [dir, dist] = line.split(' ')
            dist = int(dist)
            for _ in range(dist):
                snake[0] = add_vectors([snake[0], directions[dir]])
                for h in range(len(snake) - 1):
                    t = h + 1
                    offset = distances(snake[h], snake[t])
                    if max(map(abs, offset)) < 2:
                        continue
                    snake[t] = add_vectors([snake[t], normalize(offset)])
                visited.add(snake[-1])
    print(len(visited))

if __name__ == '__main__':
    main(2)
    main(10)

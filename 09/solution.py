from io import TextIOWrapper
from os import path
from typing import Dict, Iterable, Set, Tuple

FOLDER = path.dirname(__file__)
INPUT = path.join(FOLDER, 'input.txt')

Vector = Tuple[int, int]

directions: Dict[str, Vector] = {
    'U': (1, 0),
    'D': (-1, 0),
    'L': (0, -1),
    'R': (0, 1)
}

def line_iter(file_object: TextIOWrapper):
    for line in file_object:
        yield line.strip()

def add_vectors(iter: Iterable[Vector])-> Vector:
    x = y = 0
    for vec in iter:
        x, y = x + vec[0], y + vec[1]
    return (x, y)

def distances(vec1: Vector, vec2: Vector) -> Vector:
    x = vec1[0] - vec2[0]
    y = vec1[1] - vec2[1]
    return (x, y)

def normalize(vec: Vector) -> Vector:
    return tuple(map(lambda x : 0 if x == 0 else (1 if x > 0 else -1), vec))

def main(snake):
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
    main([ (0,0) for _ in range(2) ])
    main([ (0,0) for _ in range(10) ])

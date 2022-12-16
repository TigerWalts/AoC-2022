from functools import cache, lru_cache
from io import TextIOWrapper
from os import path
from typing import Tuple

FOLDER = path.dirname(__file__)
INPUT = path.join(FOLDER, 'input.txt')

def iter_line(file_object: TextIOWrapper):
    for line in file_object:
        yield line.strip()

@cache
def get_score(time: int, loc: int, opened: int, flows: Tuple[int], paths: Tuple[Tuple[int,...]], other: Tuple[int, int, int]):
    if time == 0:
        return 0 if other[2] == 0 else get_score(other[0], other[1], opened, flows, paths, (other[0], other[1], other[2] - 1))
    time -= 1
    moves = []
    if flows[loc] > 0 and 2**loc & opened == 0:
        moves.append(get_score(time, loc, 2**loc | opened, flows, paths, other) + (time * flows[loc]))
    for path in paths[loc]:
        moves.append(get_score(time, path, opened, flows, paths, other))
    return max(moves)

def main():
    with open(INPUT, 'r') as input_file:
        numchars = '0123456789'
        valves = {
            x[1]: {
                'flow': int(''.join(y for y in x[4] if y in numchars)),
                'paths': [ y.replace(',', '') for y in x[9:] ],
            } 
            for x
            in (
                line.split(' ')
                for line
                in iter_line(input_file)
            )
        }

    location = 'AA'
    # enumerate into tuples
    k = list(valves.keys())
    loc = k.index(location)
    opened = 0
    flows = tuple( x['flow'] for x in valves.values() )
    paths = tuple( tuple( k.index(y) for y in x['paths'] ) for x in valves.values() )

    time = 30
    print(get_score(time, loc, opened, flows, paths, (time, loc, 0)))
    time = 26
    print(get_score(time, loc, opened, flows, paths, (time, loc, 1)))

if __name__ == '__main__':
    main()
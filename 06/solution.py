from io import TextIOWrapper
from os import path
from typing import Callable, Iterable

FOLDER = path.dirname(__file__)
INPUT = path.join(FOLDER, 'input.txt')

def char_iter(file_object: TextIOWrapper):
    while True:
        char = file_object.read(1)
        if not char:
            break
        yield char

def take_n_wide(iter: Iterable, width: int) -> str:
    buf = ''
    while True:
        if len(buf) == width:
            buf = buf[1:]
        while len(buf) < width:
            try:
                buf = buf + next(iter)
            except StopIteration:
                return
        yield buf

def take_until(iter: Iterable, predicate: Callable[[any],bool]):
    while True:
        try:
            value = next(iter)
            yield value
            if predicate(value):
                raise StopIteration
        except StopIteration:
            return

def all_different(iter: Iterable) -> bool:
    listed = list(iter)
    return len(set(listed)) == len(listed)

def main(width: int):
    result = 0
    with open(INPUT, 'r') as input_file:
        take_char = char_iter(input_file)
        for index, _ in enumerate(take_until(take_n_wide(take_char, width), all_different)):
            result = index
        result += width
    print(result)

if __name__ == '__main__':
    main(4)
    main(14)
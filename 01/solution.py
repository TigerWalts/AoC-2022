from io import TextIOWrapper
from os import path
from typing import Callable, Iterable

FOLDER = path.dirname(__file__)
INPUT = path.join(FOLDER, 'input.txt')

def line_iter(file_object: TextIOWrapper):
    for line in file_object:
        yield line.strip()

def reduce_int_strings(iterator: Iterable, reduce_function: Callable[[int, int], int], terminator: str=''):
    acc = 0
    while True:
        try:
            value = iterator.__next__()
            if value == terminator:
                yield acc
                acc = 0
                continue
            acc = reduce_function(acc, int(value))
        except StopIteration:
            yield acc
            return

def top(iterator: Iterable, count: int=1):
    top = [0 for _ in range(count)]
    for candidate in iterator:
        for index, value in enumerate(top):
            if candidate > value:
                top.insert(index, candidate)
                break
        top = top[:count]
    return top

def main1():
    with open(INPUT, 'r') as input_file:
        line_gen = line_iter(input_file)
        sum_gen = reduce_int_strings(line_gen, lambda a, b: a + b )
        print(max(sum_gen))

def main2():
    with open(INPUT, 'r') as input_file:
        line_gen = line_iter(input_file)
        sum_gen = reduce_int_strings(line_gen, lambda a, b: a + b )
        print(sum(top(sum_gen, 3)))

if __name__ == "__main__":
    main1()
    main2()
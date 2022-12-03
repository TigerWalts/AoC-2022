from io import TextIOWrapper
from os import path
from typing import Iterable, Callable, Optional

FOLDER = path.dirname(__file__)
INPUT = path.join(FOLDER, 'input.txt')

PRIORITY = "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def line_iter(file_object: TextIOWrapper):
    for line in file_object:
        yield line.strip()

def take_n_iter(iterator: Iterable, count):
    while True:
        try:
            values = [ next(iterator) for _ in range(count) ]
        except StopIteration:
            break
        yield (value for value in values)

def reduce_sets(iterator: Iterable, reduce_function: Callable[[set, set], set], acc: Optional[set] = None):
    if acc is None:
        acc = {}
    for value in iterator:
        acc = reduce_function(acc, value)
    return acc

def main1():
    total = 0
    with open(INPUT) as input_file:
        for line in line_iter(input_file):
            split_index = len(line) // 2
            containers = [line[:split_index], line[split_index:]]
            sets = map(lambda c : set(x for x in c), containers)
            common = list(
                reduce_sets(
                    sets,
                    lambda a, b : a.intersection(b),
                    set(x for x in PRIORITY)
                )
            )
            total += PRIORITY.index(common[0])
    print(total)

def main2():
    total = 0
    with open(INPUT) as input_file:
        for triple_gen in take_n_iter(line_iter(input_file), 3):
            set_gen = map(set, triple_gen)
            common = list(
                reduce_sets(
                    set_gen,
                    lambda a, b : a.intersection(b),
                    set(x for x in PRIORITY)
                )
            )
            if len(common) > 0:
                total += PRIORITY.index(list(common)[0])
    print(total)

if __name__ == '__main__':
    main1()
    main2()
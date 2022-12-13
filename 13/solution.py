from functools import cmp_to_key
from io import TextIOWrapper
from os import path
from typing import Any, Callable, Iterable

FOLDER = path.dirname(__file__)
INPUT = path.join(FOLDER, 'input.txt')

def iter_line(file_object: TextIOWrapper):
    for line in file_object:
        yield line.strip()

def iter_12x(iter: Iterable):
    while True:
        yield eval(next(iter)), eval(next(iter))
        try:
            next(iter)
        except StopIteration:
            return

def iter_drop_if(iter: Iterable, drop_predicate: Callable[[Any],bool]):
    for value in iter:
        if drop_predicate(value):
            continue
        yield value

def iter_prepend(iter: Iterable, pre: Iterable):
    for value in pre:
        yield value
    for value in iter:
        yield value

def compare(left, right):
    if all(isinstance(x, int) for x in (left, right)):
        return 0 if left == right else right - left
    left, right = tuple([x] if isinstance(x, int) else x for x in (left, right))
    for result in map(lambda x : compare(*x),zip(left, right)):
        if result == 0:
            continue
        return result
    return len(right) - len(left)

def main1():
    with open(INPUT, 'r') as input_file:
        print(
            sum(
                x+1
                for x, pair
                in enumerate(
                    iter_12x(
                        iter_line(
                            input_file
                        )
                    )
                )
                if compare(*pair) > 0
            )
        )

def main2():
    with open(INPUT, 'r') as input_file:
        ordered = sorted(
            map(
                eval,
                iter_prepend(
                    ["[[2]]","[[6]]"],
                    iter_drop_if(
                        iter_line(
                            input_file
                        ),
                        lambda x : x == ''
                    )
                )
            ),
            key=cmp_to_key(compare),
            reverse=True
        )
        indexes = [
            x + 1
            for x, p
            in enumerate(ordered)
            if compare([[2]], p) == 0 or compare([[6]], p) == 0
        ]
        print(indexes[0]*indexes[1])

if __name__ == '__main__':
    main1()
    main2()

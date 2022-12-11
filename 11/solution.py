from io import TextIOWrapper
from os import path
from typing import Callable, Iterable, List, Tuple

FOLDER = path.dirname(__file__)
INPUT = path.join(FOLDER, 'input.txt')

def line_iter(file_object: TextIOWrapper):
    for line in file_object:
        yield line.strip()

def take_until(iter: Iterable, predicate: Callable[[any],bool]):
    while True:
        try:
            value = next(iter)
            yield value
            if predicate(value):
                raise StopIteration
        except StopIteration:
            return

def take_split_on(iter: Iterable, predicate: Callable[[any],bool]):
    while True:
        yield (value for value in take_until(iter, predicate))

# Monkey 0:
#   Starting items: 79, 98
#   Operation: new = old * 19
#   Test: divisible by 23
#     If true: throw to monkey 2
#     If false: throw to monkey 3
def parse_monkey(iter_lines: Iterable):
    id = None
    monkey = {}
    for line in iter_lines:
        [key, *args] = line.split(' ')
        if key == 'Monkey':
            id = args[0][:-1]
            monkey['id'] = id
        elif key == 'Starting':
            monkey['items'] = list(map(int,''.join(args[1:]).split(',')))
        elif key == 'Operation:':
            monkey['operator'] = args[3]
            monkey['operands'] = (args[2], args[4])
        elif key == 'Test:':
            monkey['divtest'] = int(args[-1])
        elif key == 'If' and args[0] == 'true:':
            monkey['if_true'] = args[-1]
        elif key == 'If' and args[0] == 'false:':
            monkey['if_false'] = args[-1]
    if len(monkey) == 0:
        raise StopIteration
    monkey['inspections'] = 0
    return id, monkey

def product(iter: Iterable[int]) -> int:
    value = 1
    for x in iter:
        value *= x
    return value

def operation_factory(operator: str, operands: Tuple, reduction: int = 1):
    OPERATIONS = {
        '*': lambda l, r : l * r,
        '/': lambda l, r : l / r,
        '+': lambda l, r : l + r,
        '-': lambda l, r : l - r
    }
    def operation(old: int):
        return OPERATIONS[operator](*map(lambda a : old if a == 'old' else int(a), operands)) // reduction
    return operation

def div_test(item, divisor):
    return item % divisor == 0

def process_monkeys(monkeys: dict, divtest_product: int, reduction: int = 1):
    for _, monkey in monkeys.items():
        items_remaindered_iter = ( item % divtest_product for item in monkey['items'] )
        items_operated_iter = map(operation_factory(monkey['operator'], monkey['operands'], reduction), items_remaindered_iter)
        items_tested_iter = ( (item, div_test(item, monkey['divtest'])) for item in items_operated_iter )
        for item, is_true in items_tested_iter:
            monkey['inspections'] += 1
            if is_true:
                monkeys[monkey['if_true']]['items'].append(item)
            if not is_true:
                monkeys[monkey['if_false']]['items'].append(item)
        monkey['items'] = []
    return monkeys

def main(rounds: int, reduction: int):
    monkeys = {}
    with open(INPUT, 'r') as input_file:
        iter_lines = line_iter(input_file)
        monkeys = { id: monkey for id, monkey in map(parse_monkey, take_split_on(iter_lines, lambda x : x == '')) if id is not None }
    divtest_product = product( monkey['divtest'] for _, monkey in monkeys.items() )
    for _ in range(rounds):
        monkeys = process_monkeys(monkeys, divtest_product, reduction)
    top_2 = sorted([monkey['inspections'] for _, monkey in monkeys.items()],reverse=True)[:2]
    print(product(top_2))

if __name__ == '__main__':
    main(20, 3)
    main(10000, 1)

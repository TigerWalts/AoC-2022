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
    return id, {
        'items': monkey['items'],
        'divtest': monkey['divtest'],
        'operation': operation_factory(monkey['operator'], monkey['operands']),
        'get_target': get_target_factory(monkey['divtest'], monkey['if_true'], monkey['if_false']),
        'inspections': 0
    }

def product(iter: Iterable[int]) -> int:
    value = 1
    for x in iter:
        value *= x
    return value

def operation_factory(operator: str, operands: Tuple):
    OPERATIONS = {
        '*': lambda l, r : l * r,
        '/': lambda l, r : l / r,
        '+': lambda l, r : l + r,
        '-': lambda l, r : l - r
    }
    def operation(old: int):
        return OPERATIONS[operator](*map(lambda a : old if a == 'old' else int(a), operands))
    return operation

def get_target_factory(divisor: int, if_true: str, if_false: str):
    def get_target(value: int):
        return if_true if value % divisor == 0 else if_false
    return get_target

def process_monkeys(monkeys: dict, divtest_product: int, reduction: int = 1):
    for _, monkey in monkeys.items():
        items_operated_iter = ( monkey['operation'](item % divtest_product) // reduction for item in monkey['items'] )
        items_targets_iter = ( (item, monkey['get_target'](item)) for item in items_operated_iter )
        for item, target in items_targets_iter:
            monkeys[target]['items'].append(item)
            monkey['inspections'] += 1
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

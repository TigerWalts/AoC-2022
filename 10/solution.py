from io import TextIOWrapper
from os import path
from typing import Callable, Iterable

FOLDER = path.dirname(__file__)
INPUT = path.join(FOLDER, 'input.txt')

def op_noop(state):
    return state

def op_addx(state, x):
    state['X'] += x
    return state

OP_CODES = {
    'noop': {
        'cycles': 1,
        'args': [],
        'action': op_noop
    },
    'addx': {
        'cycles': 2,
        'args': [int],
        'action': op_addx
    }
}

def line_iter(file_object: TextIOWrapper):
    for line in file_object:
        yield line.strip()

def process(state, commands: Iterable):
    cycle = 0
    till_free = 0
    action: Callable = op_noop
    args = []
    while True:
        cycle += 1
        if till_free > 0:
            yield cycle, state, state
            till_free -= 1
            continue
        new_state = action(state, *args)
        yield cycle, state, new_state
        state = new_state
        try:
            command = next(commands)
        except StopIteration:
            return
        [op_code, *args] = command.split(' ')
        op_sig = OP_CODES[op_code]
        till_free = op_sig['cycles'] - 1
        args = [ x[0](x[1]) for x in zip(op_sig['args'], args) ]
        action = op_sig['action']

def main():
    with open(INPUT, 'r') as input_file:
        commands = line_iter(input_file)
        state = {
            'X': 1
        }
        print(sum( x[0] * x[1]['X'] for x in process(state, commands) if (x[0] + 20) % 40 == 0 ))
        # reset
        input_file.seek(0)
        commands = line_iter(input_file)
        state = {
            'X': 1
        }
        for cycle, state, _ in process(state, commands):
            value = state['X']
            idx = (cycle - 1) % 40
            print('#' if value - 2 < idx < value + 2 else '.', end='')
            if idx == 39:
                print()

if __name__ == '__main__':
    main()
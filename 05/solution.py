from enum import Enum, auto
from io import TextIOWrapper
from os import path
from typing import List, Optional

FOLDER = path.dirname(__file__)
INPUT = path.join(FOLDER, 'input.txt')

class Parse_state(Enum):
    CRATES = auto()
    COMMANDS = auto()

class Move_type(Enum):
    SINGLE = auto()
    MULTIPLE = auto()

class Stacks:

    def __init__(self, move_type: Move_type=Move_type.SINGLE) -> None:
        self.stacks: List[List[str]] = []
        self.move_type: Move_type = move_type
    
    def add_parsed_row(self, parsed_row: List[Optional[str]]) -> None:
        for index, crate in enumerate(parsed_row):
            while len(self.stacks) - 1 < index:
                self.stacks.append([])
            if crate != ' ':
                self.stacks[index].insert(0, crate)

    def execute_parsed_command(self, command: str, count: int, from_stack: Optional[int], to_stack: Optional[int]):
        if command == 'move':
            if self.move_type == Move_type.SINGLE:
                for _ in range(count):
                    self.move_crate(from_stack, to_stack)
            if self.move_type == Move_type.MULTIPLE:
                self.move_crates(count, from_stack, to_stack)
            return
        raise ValueError(f"Command '{command}' not supported")

    def move_crate(self, from_stack: int, to_stack: int) -> None:
        self.stacks[to_stack-1].append(self.stacks[from_stack-1].pop())

    def move_crates(self, count, from_stack: int, to_stack: int) -> None:
        self.stacks[to_stack-1].extend(self.stacks[from_stack-1][-count:])
        self.stacks[from_stack-1] = self.stacks[from_stack-1][:-count]

    def top_crates(self) -> List[str]:
        return [ x[-1] for x in self.stacks if len(x) > 0 ]

def line_iter(file_object: TextIOWrapper):
    for line in file_object:
        yield line.rstrip()

def parse_row(line: str) -> List[Optional[str]]:
    if line.strip()[0] != '[':
        return []
    count = (len(line) // 4) + 1
    return [ line[(x*4)+1] for x in range(count) ]

def parse_command(line: str) -> dict:
    [command, count, _, from_stack, _, to_stack] = line.split(' ')
    return {
        'command': command,
        'count': int(count),
        'from_stack': int(from_stack),
        'to_stack': int(to_stack)
    }

def main(move_type: Move_type):
    with open(INPUT, 'r') as input_file:
        state = Parse_state.CRATES
        stacks = Stacks(move_type=move_type)
        for line in line_iter(input_file):
            if line == '':
                state = Parse_state.COMMANDS
                continue
            if state == Parse_state.CRATES:
                stacks.add_parsed_row(parse_row(line))
            if state == Parse_state.COMMANDS:
                stacks.execute_parsed_command(**parse_command(line))
        print(''.join(stacks.top_crates()))


if __name__ == '__main__':
    main(Move_type.SINGLE)
    main(Move_type.MULTIPLE)

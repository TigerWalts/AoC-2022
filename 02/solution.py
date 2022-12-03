from enum import Enum, auto
from io import TextIOWrapper
from os import path
from typing import Callable

FOLDER = path.dirname(__file__)
INPUT = path.join(FOLDER, 'input.txt')

class move_type(Enum):
    ROCK = auto()
    PAPER = auto()
    SCISSORS = auto()

MOVES = {
    'A': move_type.ROCK,
    'B': move_type.PAPER,
    'C': move_type.SCISSORS,
}

MOVE_SCORE = {
    move_type.ROCK: 1,
    move_type.PAPER: 2,
    move_type.SCISSORS: 3,
}

WHAT_LOSES_TO = {
    move_type.ROCK: move_type.SCISSORS,
    move_type.PAPER: move_type.ROCK,
    move_type.SCISSORS: move_type.PAPER,
}

WHAT_BEATS = {
    move_type.ROCK: move_type.PAPER,
    move_type.PAPER: move_type.SCISSORS,
    move_type.SCISSORS: move_type.ROCK,
}

STRATEGY1 = {
    'X': move_type.ROCK,
    'Y': move_type.PAPER,
    'Z': move_type.SCISSORS,
}

def strategy1(my_strat: str, _: move_type) -> move_type:
    return STRATEGY1[my_strat]

def strategy2(my_strat: str, move_type: move_type) -> move_type:
    if my_strat == 'X':
        # Lose
        return WHAT_LOSES_TO[move_type]
    if my_strat == 'Z':
        # Win
        return WHAT_BEATS[move_type]
    # Draw
    return move_type

def line_iter(file_object: TextIOWrapper):
    for line in file_object:
        yield line.strip()

class move:
    def __init__(self, move_type: move_type):
        self.move_type = move_type

    def move_score(self):
        return MOVE_SCORE[self.move_type]

    def __eq__(self, other):
        if not isinstance(other, move):
            other = move(other)
        return self.move_type == other.move_type

    def __gt__(self, other):
        if not isinstance(other, move):
            other = move(other)
        return self.move_type == WHAT_BEATS[other.move_type]

    def __lt__(self, other):
        if not isinstance(other, move):
            other = move(other)
        return self.move_type == WHAT_LOSES_TO[other.move_type]

def main(strat: Callable[[str, move_type], move_type]):
    opp_score = 0
    my_score = 0
    with open(INPUT, 'r') as input_file:
        for line in  line_iter(input_file):
            [opp_strat, my_strat] = list(line.split(' '))
            opp_move_type = MOVES[opp_strat]
            my_move = move(strat(my_strat, opp_move_type))
            opp_move = move(opp_move_type)
            opp_score += opp_move.move_score()
            my_score += my_move.move_score()
            if opp_move == my_move:
                opp_score += 3
                my_score += 3
            elif opp_move > my_move:
                opp_score += 6
            else:
                my_score += 6
    print(my_score)

if __name__ == '__main__':
    main(strategy1)
    main(strategy2)
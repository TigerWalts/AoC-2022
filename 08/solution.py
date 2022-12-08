from io import TextIOWrapper
from os import path, makedirs
from typing import Iterable, Optional

FOLDER = path.dirname(__file__)
DATAFOLDER = path.join(FOLDER, 'data')
INPUT = path.join(FOLDER, 'input.txt')
HSCAN = path.join(DATAFOLDER, 'h_scan.txt') # For storing horizontal scan pass
FSCAN = path.join(DATAFOLDER, 'f_scan.txt') # For debug

def line_iter(file_object: TextIOWrapper):
    for line in file_object:
        yield line

def column_iter(file_object: TextIOWrapper, column_index: int):
    file_object.seek(0)
    for line in line_iter(file_object):
        yield line[column_index]

def row_iter(file_object: TextIOWrapper, row_index: int, width: int):
    offset = row_index * (width + 2)
    file_object.seek(offset)
    for char in file_object.read(width):
        yield char

def is_max_so_far(iter: Iterable, maxval: int = -1):
    for value in iter:
        yield 1 if value > maxval else 0
        maxval = max(maxval, value)

def can_see_from_house(iter: Iterable, my_height: int, maxval: int = -1):
    for value in iter:
        if maxval >= my_height:
            return
        yield 1
        maxval = max(maxval, value)

def is_visible(iter: Iterable):
    values = list(map(int, iter))
    rtl_visible = reversed(list(is_max_so_far(reversed(values))))
    for a, b in zip(is_max_so_far(values), rtl_visible):
        yield a | b

def visible_lr(iter: Iterable, location: int):
    values = list(map(int, iter))
    my_height = values[location]
    to_left = sum(can_see_from_house([] if location == 0 else values[location-1::-1], my_height))
    to_right = sum(can_see_from_house(values[location+1:], my_height))
    return to_left, to_right

def main1():
    makedirs(DATAFOLDER, exist_ok=True)
    # Horizontal pass
    with open(INPUT, 'r') as input_file, open(HSCAN, 'w') as scan_file:
        for line in line_iter(input_file):
            end = '\n' if line[-1] == '\n' else ''
            for value in is_visible(line.strip()):
                scan_file.write(f"{value}")
            scan_file.write(end)
    # Vertical pass
    with open(INPUT, 'r') as input_file, open(HSCAN, 'r') as scan_file, open(FSCAN, 'w') as fscan_file:
        tree_sum = 0
        for y, line in enumerate(line_iter(scan_file)):
            for x, char in enumerate(line.strip()):
                if char == '1':
                    tree_sum += 1
                    fscan_file.write(f'1')
                    continue
                vis = int(list(is_visible(column_iter(input_file, x)))[y])
                fscan_file.write(f'{vis}')
                tree_sum += vis
            fscan_file.write('\n')
        print(tree_sum)

def main2():
    with open(INPUT, 'r') as input_file:
        line = input_file.readline()
        size = len(line)
        width = len(line.strip())
        while True:
            chunk = input_file.read(128)
            if not len(chunk):
                break
            size += len(chunk)
        size += 1
        height = size // (width + 1)
        max_val = 0
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                left, right = visible_lr(row_iter(input_file, y, width), x)
                top, bottom = visible_lr(column_iter(input_file, x), y)
                value = top * bottom * left * right
                max_val = max(max_val, value)
        print(max_val)

if __name__ == '__main__':
    main1()
    main2()

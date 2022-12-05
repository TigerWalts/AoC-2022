from io import TextIOWrapper
from os import path

FOLDER = path.dirname(__file__)
INPUT = path.join(FOLDER, 'input.txt')

def line_iter(file_object: TextIOWrapper):
    for line in file_object:
        yield line.strip()

def main1():
    count = 0
    with open(INPUT, 'r') as input_file:
        for line in line_iter(input_file):
            [elf1_str, elf2_str] = line.split(',')
            [elf1_start, elf1_end] = list(map(int,elf1_str.split('-')))
            [elf2_start, elf2_end] = list(map(int,elf2_str.split('-')))
            if (
                (
                    elf1_start <= elf2_start and elf1_end >= elf2_end
                ) or (
                    elf2_start <= elf1_start and elf2_end >= elf1_end
                )
            ):
                count += 1
    print(count)


def main2():
    count = 0
    with open(INPUT, 'r') as input_file:
        for line in line_iter(input_file):
            [elf1_str, elf2_str] = line.split(',')
            [elf1_start, elf1_end] = list(map(int,elf1_str.split('-')))
            [elf2_start, elf2_end] = list(map(int,elf2_str.split('-')))
            if (
                (
                    elf2_start <= elf1_start <= elf2_end
                ) or (
                    elf2_start <= elf1_end <= elf2_end
                ) or (
                    elf1_start <= elf2_start <= elf1_end
                ) or (
                    elf1_start <= elf2_end <= elf1_end
                )
            ):
                count += 1
    print(count)

if __name__ == '__main__':
    main1()
    main2()
from io import TextIOWrapper
from os import path

FOLDER = path.dirname(__file__)
INPUT = path.join(FOLDER, 'input_example.txt')

def iter_line(file_object: TextIOWrapper):
    for line in file_object:
        yield line.strip()

def main():
    with open(INPUT, 'r') as input_file:
        pass

if __name__ == '__main__':
    main()
from __future__ import annotations
from enum import Enum
from io import TextIOWrapper
from os import path
from typing import List, Optional

FOLDER = path.dirname(__file__)
INPUT = path.join(FOLDER, 'input.txt')

def line_iter(file_object: TextIOWrapper):
    for line in file_object:
        yield line.strip()

class FileType(Enum):
    FOLDER = 'dir'
    FILE = 'file'

class FileNode():
    
    def __init__(self, name: str, file_type: FileType, size: int, parent: Optional[FileNode] = None):
        self.name: str = name
        self.file_type: FileType = file_type
        self.size: int = size
        self.children: List[FileNode] = []
        self.parent: Optional[FileNode] = parent

    def change_directory(self, arg: str) -> FileNode:
        if arg == '/' and self.parent is None:
            return self
        if arg == '/':
            self.parent.change_directory('/')
        if arg == '..' and self.parent is None:
            raise ValueError("Cannot execute 'cd ..', already at root")
        if arg == '..':
            return self.parent
        candidates = list(filter(lambda x : x.name == arg and x.file_type == FileType.FOLDER , self.children))
        if len(candidates) > 1:
            raise ValueError(f"Cannote execute 'cd {arg}', found {len(candidates)} folders with that name!")
        if len(candidates) == 1:
            return candidates[0]
        self.add_folder(arg)
        return self.children[-1]

    def add_folder(self, name: str):
        self.children.append(FileNode(name, FileType.FOLDER, 0, self))

    def add_file(self, name: str, size: int):
        self.children.append(FileNode(name, FileType.FILE, size, self))

    def get_path(self) -> List[str]:
        if self.parent is None:
            return [self.name]
        else:
            return self.parent.get_path() + [self.name]

    def get_size(self) -> int:
        return self.size + sum(child.get_size() for child in self.children)

    def walk(self):
        for child in self.children:
            yield child.name, child.file_type, child.get_size()
            if child.file_type == FileType.FOLDER:
                for gchild in child.walk():
                    yield gchild

    def __str__(self):
        newline = '\n'
        depth = len(self.get_path())
        children = newline.join('  '*depth + str(child) for child in self.children)
        attrs = f"{self.file_type.value}{'' if self.file_type == FileType.FOLDER else f' size={self.size}'}"
        return f"- {self.name} ({attrs}){newline if len(children) else ''}{children}"
    
    def __repr__(self):
        return f"FileNode(name={self.name}, file_type={self.file_type}, size={self.size}, path={self.get_path()}, children={[x.name for x in self.children]})"

def main():
    root = current_node = FileNode('/', FileType.FOLDER, 0)
    with open(INPUT, 'r') as input_file:
        iter_lines = line_iter(input_file)
        last_command = None
        for line in iter_lines:
            if line[0] == '$':
                [_, last_command, *args] = line.split(' ')
                if last_command == 'cd':
                    current_node = current_node.change_directory(args[0])
                continue
            if last_command == 'ls':
                [size, name, *_] = line.split(' ')
                if size == 'dir':
                    current_node.add_folder(name)
                else:
                    current_node.add_file(name, int(size))
    print(sum(x[2] for x in filter(lambda x : x[1] == FileType.FOLDER and x[2] <= 100000, root.walk())))
    disk_size = 70_000_000
    target_usage = disk_size - 30_000_000
    free_at_least = root.get_size() - target_usage
    print(min(x[2] for x in filter(lambda x : x[1] == FileType.FOLDER and x[2] >= free_at_least, root.walk())))

if __name__ == '__main__':
    main()

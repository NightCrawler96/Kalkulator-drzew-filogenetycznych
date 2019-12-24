from typing import List

from newick import loads, read, Node, write


def load_from_string(tree: str):
    return loads(tree)


def load_from_file(file_name: str):
    return read(file_name)


def write_to_file(tree: List[Node], file_name: str):
    write(tree, file_name)

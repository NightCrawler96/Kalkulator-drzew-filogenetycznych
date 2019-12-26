import re
import string
from random import choice

from newick import dumps

from actions import ask_if_finished, get_integer
from phylogenetic_trees.trees import PhyTree


def modify(file_name: str, tree: PhyTree):
    finished = False
    while not finished:
        print("Tree has following groups:")
        print(tree.get_nodes())
        print("Add leaf:")
        node = input()
        if re.match(r"[{} ]", node):
            print("Leaf name can not include {, }, and space")
            continue
        print(f"Add leaf '{node}' to group:")
        group = input()
        if not re.match(r'[{}]', group):
            print("Target group has to be enclosed by {} brackets")
            continue
        current_structure = dumps(tree.get_newick())
        try:
            tree.add_to_group(node, group)
        except ValueError as e:
            print(e)
            tree.parse_string(current_structure)
        finished = ask_if_finished()
    tree.save(file_name)


def create(file_name: str):
    tree = PhyTree()
    modify(file_name, tree)


def update(file_name: str):
    tree = PhyTree()
    tree.load_file(file_name)
    modify(file_name, tree)


def random_tree(file_name: str, leaves_num: int = 0):
    if leaves_num == 0:
        print("Number of leaves:")
        leaves_num = get_integer()

    leaves_queue = string.ascii_uppercase[:leaves_num]

    tree = PhyTree()
    for l in leaves_queue:
        available_nodes = list(filter(lambda n: re.match(r"{[a-zA-Z0-9]*}", n), tree.get_nodes()))
        chosen_node = choice(available_nodes)
        tree.add_to_group(l, chosen_node)

    tree.save(file_name)

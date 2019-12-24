import re

from actions import ask_if_finished
from phylogenetic_trees.trees import PhyTree


def create(file_name: str):
    tree = PhyTree()
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
        try:
            tree.add_to_group(node, group)
        except ValueError as e:
            print(e)
        finished = ask_if_finished()
    tree.save(file_name)


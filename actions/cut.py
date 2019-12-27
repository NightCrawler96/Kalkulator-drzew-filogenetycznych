import os

from actions import ask_if_finished
from phylogenetic_trees.cutting import TreeCutter
from phylogenetic_trees.trees import PhyTree


def cut(file_name: str):
    if not os.path.isfile(file_name):
        print("Given file has to exist.")
        return
    tree = PhyTree()
    tree.load_file(file_name)
    wanted_leaves = set()
    choose_leaves = True
    while choose_leaves:
        print(f"Chosen leaves: {wanted_leaves}")
        leaf = input("Add leaf: ")
        if leaf not in tree.leaves:
            print(f"{leaf} was not among the tree's leaves")
            continue
        if leaf in wanted_leaves:
            print(f"{leaf} is already among wanted leaves")
            continue
        wanted_leaves.add(leaf)
        choose_leaves = not ask_if_finished()
    cutter = TreeCutter()
    cutter.attach_tree(tree)
    cutter.choose_leaves(wanted_leaves)
    new_tree = cutter.cut()
    new_tree.save(file_name)

import os

from actions import ask_if_finished, get_float, get_file_path
from phylogenetic_trees.compare import consensus, rf_distance
from phylogenetic_trees.trees import PhyTree


def consensus_tree():
    trees = []
    add_trees = True
    while add_trees:
        try:
            phy_tree = PhyTree()
            path = input("Tree's path: ")
            if os.path.isdir(path):
                files = os.listdir(path)
                for f in files:
                    p = PhyTree()
                    p.load_file(path + f)
                    trees.append(p)
                break
            else:
                phy_tree.load_file(path)
        except ValueError as e:
            print(e)
            continue
        trees.append(phy_tree)
        add_trees = not ask_if_finished()
    print("Threshold:")
    threshold = get_float()

    result = consensus(trees, threshold)
    path = input("Save as: ")
    result.save(path)


def rf_distance_cmd():
    print("First tree:")
    left = get_file_path()
    print("Second tree:")
    right = get_file_path()
    left_tree = PhyTree()
    left_tree.load_file(left)
    right_tree = PhyTree()
    right_tree.load_file(right)
    distance = rf_distance(left_tree, right_tree)
    print(f"Distance: {distance}")

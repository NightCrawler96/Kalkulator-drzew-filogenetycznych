from actions import ask_if_finished, get_float
from phylogenetic_trees.compare import consensus
from phylogenetic_trees.trees import PhyTree


def consensus_tree():
    trees = []
    add_trees = True
    while add_trees:
        try:
            phy_tree = PhyTree()
            path = input("Tree's path: ")
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

from philogenetic_trees.io import load_from_string
from philogenetic_trees.visualization import visualize_tree

if __name__ == "__main__":
    tree = load_from_string("((A, B, C){A B C}, (D, E){D E}, (F, G){F G}){A B C D E F G};")
    visualize_tree(tree[0])

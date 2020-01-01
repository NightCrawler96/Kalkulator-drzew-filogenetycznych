from typing import List, Set

from phylogenetic_trees.trees import PhyTree, phytree_from_groups, bipartitions


def consensus(trees: List[PhyTree], threshold: float) -> PhyTree:
    assert 0.5 <= threshold < 1

    def set_or_add(dictionary: dict, key: str):
        if key in dictionary.keys():
            dictionary[key] += 1
        else:
            dictionary[key] = 1

    clusters = dict()
    for t in trees:
        groups = t.get_nodes()
        for g in groups:
            set_or_add(clusters, g)
    clusters = {c: x/len(trees) for c, x in clusters.items()}
    clusters = list(dict(filter(lambda i: i[1] > threshold, clusters.items())).keys())

    return phytree_from_groups(clusters)


def rf_distance(tree_left: PhyTree, tree_right: PhyTree) -> int:
    left_bp = bipartitions(tree_left)
    right_bp = bipartitions(tree_right)
    diff = [bp for bp in left_bp if bp not in right_bp] + [bp for bp in right_bp if bp not in left_bp]
    return 2 * len(diff)

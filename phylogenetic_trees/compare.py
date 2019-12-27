import re
from typing import List

from newick import Node

from phylogenetic_trees.trees import PhyTree, phytree_from_groups


def compare_groups(group_left: List[str], group_right: List[str]):
    common_nodes = set(group_left) & set(group_right)


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

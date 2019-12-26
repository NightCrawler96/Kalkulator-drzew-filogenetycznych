import re
from typing import List

from newick import Node

from phylogenetic_trees.trees import PhyTree


def compare_groups(group_left: List[str], group_right: List[str]):
    common_nodes = set(group_left) & set(group_right)


def consensus(trees: List[PhyTree], threshold: float) -> PhyTree:
    assert 0 < threshold < 1

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
    clusters = dict(filter(lambda i: i[1] > threshold, clusters.items())).keys()
    # TODO: Find overlapping clusters and solve te overlap i.e.: {A B C}:.6 and {C D}:.7 -> {A B} and {C D}
    # TODO: Sort clusters by length -> find dependencies between clusters -> connect them to a tree
    cluster_sets = [set(filter(lambda x: re.match(r'[a-zA-Z0-9]+', x), set(c))) for c in clusters]
    cluster_sets = sorted(cluster_sets, key=lambda x: len(x), reverse=True)
    leaves = set()
    for c in cluster_sets:
        leaves = leaves | c
    pass


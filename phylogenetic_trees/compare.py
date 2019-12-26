import re
from typing import List

from newick import Node

from phylogenetic_trees.trees import PhyTree


def compare_groups(group_left: List[str], group_right: List[str]):
    common_nodes = set(group_left) & set(group_right)


def consensus(trees: List[PhyTree], threshold: float) -> PhyTree:
    assert 0.5 <= threshold < 1

    def set_or_add(dictionary: dict, key: str):
        if key in dictionary.keys():
            dictionary[key] += 1
        else:
            dictionary[key] = 1

    class TreeBlock:
        name: set
        contains: List[str]

        def __init__(self, name: set):
            self.name = name
            self.contains = []

        def name_to_str(self) -> str:
            name_str = re.sub(r"[,']", "", str(sorted(self.name))).replace("[", "{").replace("]", "}")
            return name_str

        def __str__(self):
            return f"Group: {self.name}, Contains: {self.contains}"

    clusters = dict()
    for t in trees:
        groups = t.get_nodes()
        for g in groups:
            set_or_add(clusters, g)
    clusters = {c: x/len(trees) for c, x in clusters.items()}
    clusters = dict(filter(lambda i: i[1] > threshold, clusters.items())).keys()
    cluster_sets = [set(filter(lambda x: re.match(r'[a-zA-Z0-9]+', x), set(c))) for c in clusters]
    cluster_sets = sorted(cluster_sets, key=lambda x: len(x), reverse=True)
    blocks = [TreeBlock(s) for s in cluster_sets]
    for b in blocks:
        for other_block in blocks:
            if b.name > other_block.name:
                b.contains.append(other_block.name_to_str())
    blocks = list(sorted(blocks, key=lambda b: len(b.contains)))
    nodes: List[Node] = []
    for b in blocks:
        node = Node(b.name_to_str())
        for d in b.contains:
            descendant = list(filter(lambda n: n.name == d, nodes))
            if len(descendant) > 0:
                node.descendants.append(descendant[0])
                node.descendants = list(sorted(node.descendants, key=lambda d: d.name))
                nodes.remove(descendant[0])
        nodes.append(node)
    return PhyTree(nodes)


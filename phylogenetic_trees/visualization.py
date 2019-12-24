from typing import List
import matplotlib.pyplot as plt
import networkx as nx
from newick import Node

from phylogenetic_trees.trees import PhyTree


def _position_vertices(root: Node, available_space: float) -> List[tuple]:
    my_position = 0
    children = root.descendants
    space_per_child = available_space / len(children) if len(children) > 0 else 0.
    known_positions = [(0, my_position)]
    for ch, bias in zip(children, range(len(children))):
        child_positions = _position_vertices(ch, space_per_child)
        child_positions = [(x + 1, y + bias * space_per_child) for x, y in child_positions]
        known_positions += child_positions

    return known_positions


def visualize_tree(root: Node):
    v, e = PhyTree._get_nodes(root)
    graph = nx.DiGraph()
    graph.add_edges_from(e)
    positions = _position_vertices(root, 1)
    positions = {node: (x * 10, y * len(v) / 2) for node, (x, y) in zip(v, positions)}

    nx.draw(
        graph,
        positions,
        node_size=(250 * len(v)),
        font_size=6,
        with_labels=True)
    plt.show()

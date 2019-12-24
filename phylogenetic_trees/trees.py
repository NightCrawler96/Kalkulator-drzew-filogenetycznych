import re
from typing import List

from newick import Node

from phylogenetic_trees.io import load_from_file, load_from_string, write_to_file


class PhyTree:
    def __init__(self, newick_tree: List[Node] = None):
        if newick_tree is not None:
            self._check_and_load(newick_tree)
        else:
            self._newick_tree = None
            self.leaves = []

    def _check_and_load(self, tree: List[Node]):
        if PhyTree.check_tree(tree):
            self._newick_tree = tree
            self.leaves = PhyTree._get_leaves(tree)
        else:
            raise ValueError("Given tree is not correct")

    @staticmethod
    def _get_leaves(tree: List[Node]) -> List[str]:
        vertices, _ = PhyTree._get_nodes(tree[0])
        leaves = list(filter(lambda v: not PhyTree._is_group(v), vertices))
        if leaves is []:
            raise ValueError("Given tree has no legit leaves")
        return leaves

    @staticmethod
    def _is_group(node: str):
        return bool(re.match(r'{(\ ?[a-zA-Z0-9]+){2,}}$', node))

    @staticmethod
    def _get_group_leaves(group: str):
        matches = re.findall(r'[a-zA-Z]+', group)
        return matches

    @staticmethod
    def _check_group(root: Node):
        if not PhyTree._is_group(root.name):
            raise ValueError(f"{root.name} is not a group")
        children = set(root.descendants)
        leaves = PhyTree._get_group_leaves(root.name)
        expected_leaves = set(leaves)
        known_leaves = set(leaves[:])

        for ch in children:
            ch_name: str = ch.name

            if PhyTree._is_group(ch_name):
                ch_leaves = set(PhyTree._get_group_leaves(ch_name))
                if ch_leaves <= expected_leaves:
                    expected_leaves -= ch_leaves
                elif ch_leaves <= known_leaves:
                    raise ValueError("Single leaf can not appear in more than one node in a tree layer")
                else:
                    raise ValueError(f"Group {ch_name} has node that is not a leaf")
            else:
                ch_name = re.sub(r'{|}', "", ch_name)
                if ch_name in expected_leaves:
                    expected_leaves.remove(ch_name)
                else:
                    raise ValueError(f"{ch_name} is not a leaf")

        if len(expected_leaves) > 0:
            raise ValueError(f"{expected_leaves} are not among the child nodes")

    @staticmethod
    def _check_next_node(node: Node):
        if PhyTree._is_group(node.name):
            PhyTree._check_group(node)
            for child in node.descendants:
                PhyTree._check_next_node(child)

    @staticmethod
    def check_tree(tree: List[Node]) -> bool:
        try:
            PhyTree._check_next_node(tree[0])
        except ValueError as e:
            print(e)
            return False

        return True

    def load_file(self, file_name: str):
        tree = load_from_file(file_name)
        self._check_and_load(tree)

    def parse_string(self, text: str):
        tree = load_from_string(text)
        self._check_and_load(tree)

    def save(self, file_name: str):
        write_to_file(self._newick_tree, file_name)

    def get_newick(self) -> List[Node]:
        return self._newick_tree

    @staticmethod
    def _get_nodes(node: Node):
        vertices = [node.name]
        edges = []

        for child in node.descendants:
            edges.append((node.name, child.name))
            child_vertices, child_edges = PhyTree._get_nodes(child)
            if child_vertices is not []:
                vertices += child_vertices
                edges += child_edges

        return vertices, edges

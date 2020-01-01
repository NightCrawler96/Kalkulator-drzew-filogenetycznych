import re
from typing import List, Tuple, Set

from newick import Node

from phylogenetic_trees.io import load_from_file, load_from_string, write_to_file


class PhyTree:
    leaves: set

    def __init__(self, newick_tree: List[Node] = None):
        if newick_tree is not None:
            self._check_and_load(newick_tree)
        else:
            self._newick_tree = load_from_string("{};")
            self.leaves = set()

    @staticmethod
    def check_tree(tree: List[Node]):
        PhyTree._check_next_node(tree[0])

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

    def get_nodes(self):
        groups, _ = self._get_structure(self._newick_tree[0])
        return groups

    def get_clusters(self):
        groups = self.get_nodes()
        return list(filter(lambda n: not re.match(r"{[a-zA-Z0-9]*}", n), groups))

    def add_to_group(self, leaf: str, group: str):
        if not (PhyTree._is_group(group) or PhyTree._is_leaf(group)):
            raise ValueError(f"{group} is not a group nor a leaf")
        elif leaf in self.leaves:
            raise ValueError(f"{leaf} is already added to a tree")
        else:
            PhyTree._add_leaf(self._newick_tree[0], group, leaf)
            self.check_tree(self._newick_tree)
            self.leaves.add(leaf)

    @staticmethod
    def _add_leaf(node: Node, target: str, leaf: str):
        if PhyTree._is_group(node.name):
            if node.name == target:
                node.add_descendant(Node(f"{{{leaf}}}"))
            else:
                if PhyTree._is_group(target):
                    expected_leaves = set(PhyTree._get_group_leaves(target))
                else:
                    expected_leaves = {target}
                for child in node.descendants:
                    if PhyTree._is_group(child.name):
                        child_leaves = set(PhyTree._get_group_leaves(child.name))
                        if expected_leaves <= child_leaves:
                            PhyTree._add_leaf(child, target, leaf)
                            break
                    elif PhyTree._is_leaf(child.name):
                        if child.name in expected_leaves:
                            PhyTree._add_leaf(child, target, leaf)
                    else:
                        raise ValueError(f"Couldn't find {target}")

        elif PhyTree._is_leaf(node.name):
            if node.name == target:
                if node.name != '{}':
                    node.add_descendant(Node(node.name))
                    node.add_descendant(Node(f"{{{leaf}}}"))
                else:
                    node.name = f"{{{leaf}}}"
                    return
            else:
                raise ValueError(f"Unexpected leaf: {node.name}")
        else:
            raise ValueError(f"Couldn't recognize {leaf} as a leaf or a group")
        node.name = node.name.replace("}", f" {leaf}}}")

    def _check_and_load(self, tree: List[Node]):
        try:
            PhyTree.check_tree(tree)
            self._newick_tree = tree
            self.leaves, self.groups = PhyTree._get_leaves_and_groups(tree)
            self.leaves = {re.sub(r'{|}', "", leaf) for leaf in self.leaves}
        except ValueError as reason:
            raise ValueError("Given tree is not correct\n" + str(reason.args[0]))

    @staticmethod
    def _is_leaf(node: str):
        return re.match(r'{([a-zA-Z0-9]+|)}', node)

    @staticmethod
    def _get_leaves_and_groups(tree: List[Node]) -> (set, set):
        vertices, _ = PhyTree._get_structure(tree[0])
        if len(vertices) < 2:
            return vertices, set()
        leaves = set(filter(lambda v: not PhyTree._is_group(v), vertices))
        groups = set(filter(lambda v: PhyTree._is_group(v), vertices))
        if len(leaves) < 1:
            raise ValueError("Given tree has no legit leaves")
        elif len(groups) < 1:
            raise ValueError("No groups were find inside a tree")
        return leaves, groups

    @staticmethod
    def _is_group(node: str):
        return bool(re.match(r'{(\ ?[a-zA-Z0-9]+){2,}}$', node))

    @staticmethod
    def _get_group_leaves(group: str, add_brackets: bool = True):
        matches = re.findall(r'[a-zA-Z0-9]+', group)
        if add_brackets:
            matches = [f"{{{l}}}" for l in matches]
        return matches

    @staticmethod
    def _check_group(root: Node):
        if not PhyTree._is_group(root.name):
            raise ValueError(f"{root.name} is not a group nor a leaf")
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
                if ch_name in expected_leaves:
                    expected_leaves.remove(ch_name)
                else:
                    raise ValueError(f"{ch_name} is not a leaf or is duplicated")

        if len(expected_leaves) > 0:
            raise ValueError(f"{expected_leaves} are not among the child nodes")

    @staticmethod
    def _check_next_node(node: Node):
        if PhyTree._is_group(node.name):
            PhyTree._check_group(node)
            for child in node.descendants:
                PhyTree._check_next_node(child)

    @staticmethod
    def _get_structure(node: Node) -> (List[str], List[str]):
        vertices = [node.name]
        edges = []

        for child in node.descendants:
            edges.append((node.name, child.name))
            child_vertices, child_edges = PhyTree._get_structure(child)
            if child_vertices is not []:
                vertices += child_vertices
                edges += child_edges

        return vertices, edges


def phytree_from_groups(groups: List[set]):
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

    cluster_sets = [set(filter(lambda x: re.match(r'[a-zA-Z0-9]+', x), set(c))) for c in groups]
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


def bipartitions(tree: PhyTree) -> List[tuple]:
    root = tree.get_newick()[0]
    _, edges = PhyTree._get_structure(root)
    leaves = set(PhyTree._get_group_leaves(root.name, add_brackets=False))
    partitions = []
    for e in edges:
        child_leaves = set(PhyTree._get_group_leaves(e[1], add_brackets=False))
        rest = leaves - child_leaves
        if len(child_leaves) > len(rest):
            b = rest.copy()
            rest = child_leaves.copy()
            child_leaves = b
        if (child_leaves, rest) not in partitions and (rest, child_leaves) not in partitions:
            partitions.append((rest, child_leaves))

    return partitions


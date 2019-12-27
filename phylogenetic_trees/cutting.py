import re

from phylogenetic_trees.trees import PhyTree, phytree_from_groups


class TreeCutter:
    _tree: PhyTree
    _leaves: set

    def attach_tree(self, tree: PhyTree) -> None:
        self._tree = tree

    def choose_leaves(self, leaves: set) -> None:
        assert len(leaves) > 0
        assert self._tree.leaves >= leaves
        self._leaves = leaves

    def cut(self) -> PhyTree:
        assert self._tree is not None
        assert self._leaves is not None and len(self._leaves) > 0

        groups = self._tree.get_nodes()
        group_sets = [set(filter(lambda x: re.match(r'[a-zA-Z0-9]+', x), set(c))) for c in groups]
        new_groups = list()
        for g in group_sets:
            new_g = g & self._leaves
            if len(new_g) > 0 and new_g not in new_groups:
                new_groups.append(new_g)

        return phytree_from_groups(list(new_groups))

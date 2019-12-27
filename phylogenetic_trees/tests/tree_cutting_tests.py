import unittest

from newick import loads

from phylogenetic_trees.cutting import TreeCutter
from phylogenetic_trees.tests import compare_nodes
from phylogenetic_trees.trees import PhyTree


class TreeCutterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tree = PhyTree(loads("({A},({B},{C}){B C},({D},({E},{F}){E F}){D E F}){A B C D E F};"))

    def test_cut_leaf_from_first_layer(self):
        # cut A
        leaves = {'B', 'C', 'D', 'E', 'F'}
        expected_tree = loads("(({B},{C}){B C},({D},({E},{F}){E F}){D E F}){B C D E F};")

        cutter = TreeCutter()
        cutter.attach_tree(self.tree)
        cutter.choose_leaves(leaves)
        result = cutter.cut()
        compare_nodes(self, result.get_newick()[0], expected_tree[0])

    def test_cut_leaf_from_two_parts_group(self):
        # cut E
        leaves = {'A', 'B', 'C', 'D', 'F'}
        expected_tree = loads("({A},({B},{C}){B C},({D},{F}){D F}){A B C D F};")
        cutter = TreeCutter()
        cutter.attach_tree(self.tree)
        cutter.choose_leaves(leaves)
        result = cutter.cut()
        compare_nodes(self, result.get_newick()[0], expected_tree[0])

    def test_cut_leaf_from_second_layer(self):
        # cut D
        leaves = {'A', 'B', 'C', 'E', 'F'}
        expected_tree = loads("({A},({B},{C}){B C},({E},{F}){E F}){A B C E F};")
        cutter = TreeCutter()
        cutter.attach_tree(self.tree)
        cutter.choose_leaves(leaves)
        result = cutter.cut()
        compare_nodes(self, result.get_newick()[0], expected_tree[0])

    def test_cut_whole_branch(self):
        # cut {B C}
        leaves = {'A', 'D', 'E', 'F'}
        expected_tree = loads("({A},({D},({E},{F}){E F}){D E F}){A D E F};")
        cutter = TreeCutter()
        cutter.attach_tree(self.tree)
        cutter.choose_leaves(leaves)
        result = cutter.cut()
        compare_nodes(self, result.get_newick()[0], expected_tree[0])

    def test_cut_sub_branch(self):
        # cut {E F}
        leaves = {'A', 'B', 'C', 'D'}
        expected_tree = loads("({A},({B},{C}){B C},{D}){A B C D};")
        cutter = TreeCutter()
        cutter.attach_tree(self.tree)
        cutter.choose_leaves(leaves)
        result = cutter.cut()
        compare_nodes(self, result.get_newick()[0], expected_tree[0])

    def test_reduce_to_one_leaf(self):
        # reduce to A
        leaves = {'A'}
        expected_tree = loads("{A};")
        cutter = TreeCutter()
        cutter.attach_tree(self.tree)
        cutter.choose_leaves(leaves)
        result = cutter.cut()
        compare_nodes(self, result.get_newick()[0], expected_tree[0])

    def test_reduce_to_sub_branch(self):
        # reduce to {E F}
        leaves = {'E', 'F'}
        expected_tree = loads("({E},{F}){E F};")
        cutter = TreeCutter()
        cutter.attach_tree(self.tree)
        cutter.choose_leaves(leaves)
        result = cutter.cut()
        compare_nodes(self, result.get_newick()[0], expected_tree[0])


if __name__ == '__main__':
    unittest.main()
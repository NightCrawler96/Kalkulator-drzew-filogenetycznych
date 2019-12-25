import unittest
from unittest import TestCase

from newick import loads, Node

from phylogenetic_trees.trees import PhyTree


class PhiTreeParsingTrees(unittest.TestCase):
    def test_detect_group(self):
        group = "{Item Item}"

        self.assertTrue(PhyTree._is_group(group))

    def test_is_not_group(self):
        group = "{Item Item"

        self.assertFalse(PhyTree._is_group(group))

    def test_get_leaves(self):
        tree = loads("(({A},{B}){A B},({C},{D}){C D}){A B C D};")
        leaves = ["{A}", "{B}", "{C}", "{D}"]
        received_leaves , _ = PhyTree._get_leaves_and_groups(tree)
        self.assertListEqual(received_leaves, leaves)

    def test_leaves_inside_group(self):
        group = "{A B C D}"
        leaves = ["{A}", "{B}", "{C}", "{D}"]

        self.assertListEqual(PhyTree._get_group_leaves(group), leaves)

    def test_check_group(self):
        tree = loads("({A},({B},{C}){B C},{D}){A B C D};")

        try:
            PhyTree._check_group(tree[0])
        except ValueError:
            raise AssertionError()

    def test_check_group_fails(self):
        bad_groups = [
            "({A},{A B}){A B};",
            "({A},{B},{C}){A B};",
            "({A},{B}){A B C};",
            "({A},{A},{B}){A B};"
            "{A};"
        ]

        for t in bad_groups:
            with self.assertRaises(ValueError):
                PhyTree._check_group(loads(t)[0])

    def test_correct_tree(self):
        tree = loads("({A},({B},({C},{D}){C D}){B C D},{E}){A B C D E};")

        try:
            PhyTree(tree)
        except ValueError:
            raise AssertionError()

    def test_bad_tree(self):
        bad_trees = [
            "(({B},({C},{D}){C D}){B C D},{E}){A B C D E};",
            "({A},({B},{C D}){B C D},{E}){A B C D E};",
            "({A},({B},({C},{D}){C D}){B C D},E){A B C};",
            "({A},({B},({C},{D}){C D}){B X D},{E}){A B C D E};",
        ]

        for t in bad_trees:
            with self.assertRaises(ValueError):
                PhyTree(loads(t))


class PhyTreeStructureManipulation(TestCase):
    def compare_nodes(self, node0: Node, node1: Node):
        self.assertEqual(node0.name, node1.name)
        for ch0, ch1 in zip(node0.descendants, node1.descendants):
            self.compare_nodes(ch0, ch1)

    def test_add_leaf_new_group(self):
        old_tree = "(({A},{B}){A B},{C}){A B C};"
        new_tree = "(({A},({B},{X}){B X}){A B X},{C}){A B C X};"
        olf_phy, new_phy = PhyTree(), PhyTree()
        olf_phy.parse_string(old_tree)
        new_phy.parse_string(new_tree)

        olf_phy.add_to_group("X", "{B}")

        old_newick, new_newick = olf_phy.get_newick(), new_phy.get_newick()
        self.compare_nodes(old_newick[0], new_newick[0])

    def test_add_leaf_append_group(self):
        old_tree = "(({A},{B}){A B},{C}){A B C};"
        new_tree = "(({A},{B},{X}){A B X},{C}){A B C X};"
        olf_phy, new_phy = PhyTree(), PhyTree()
        olf_phy.parse_string(old_tree)
        new_phy.parse_string(new_tree)

        olf_phy.add_to_group("X", "{A B}")

        old_newick, new_newick = olf_phy.get_newick(), new_phy.get_newick()
        self.compare_nodes(old_newick[0], new_newick[0])

    def test_create_new_tree(self):
        starting_root = "{};"
        first_leaf = "{A};"

        phy_tree = PhyTree(loads(starting_root))
        phy_tree.add_to_group("A", "{}")
        self.compare_nodes(phy_tree.get_newick()[0], loads(first_leaf)[0])

    def test_add_second_leaf(self):
        starting_point = "{A};"
        expected_tree = "({A},{B}){A B};"

        phy_tree = PhyTree(loads(starting_point))
        phy_tree.add_to_group("B", "{A}")
        self.compare_nodes(phy_tree.get_newick()[0], loads(expected_tree)[0])

    def test_add_second_level(self):
        starting_point = "({A},{B}){A B};"
        expected_tree = "({A},({B},{C}){B C}){A B C};"

        phy_tree = PhyTree(loads(starting_point))
        phy_tree.add_to_group("C", "{B}")
        self.compare_nodes(phy_tree.get_newick()[0], loads(expected_tree)[0])

    def test_no_leaves_with_the_same_name(self):
        starting_point = "({A},({B},{D}){B D},{C}){A B C D};"
        phy_tree = PhyTree(loads(starting_point))
        with self.assertRaises(ValueError):
            phy_tree.add_to_group("D", "{A}")


if __name__ == '__main__':
    unittest.main()

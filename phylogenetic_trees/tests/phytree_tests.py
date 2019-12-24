import unittest

from newick import loads

from phylogenetic_trees.trees import PhyTree


class PhiTreeParsingTrees(unittest.TestCase):
    def test_detect_group(self):
        group = "{Item Item}"

        self.assertTrue(PhyTree._is_group(group))

    def test_is_not_group(self):
        group = "{Item Item"

        self.assertFalse(PhyTree._is_group(group))

    def test_get_leaves(self):
        tree = loads("((A, B){A B},(C, D){C D}){A B C D};")
        leaves = ["A", "B", "C", "D"]

        self.assertListEqual(PhyTree._get_leaves(tree), leaves)

    def test_leaves_inside_group(self):
        group = "{A B C D}"
        leaves = ["A", "B", "C", "D"]

        self.assertListEqual(PhyTree._get_group_leaves(group), leaves)

    def test_check_group(self):
        tree = loads("(A,(B,C){B C},D){A B C D};")

        try:
            PhyTree._check_group(tree[0])
        except ValueError:
            raise AssertionError()

    def test_check_group_fails(self):
        bad_groups = [
            "(A,{A B}){A B};",
            "(A,B,C){A B};",
            "(A,B){A B C};",
            "(A,A,B){A B};"
            "A;"
        ]

        for t in bad_groups:
            with self.assertRaises(ValueError):
                PhyTree._check_group(loads(t)[0])

    def test_correct_tree(self):
        tree = loads("(A,(B,(C,D){C D}){B C D},E){A B C D E};")

        try:
            PhyTree(tree)
        except ValueError:
            raise AssertionError()

    def test_bad_tree(self):
        bad_trees = [
            "((B,(C D){C D}){B C D},E){A B C D E};",
            "(A,(B,{C D}){B C D},E){A B C D E};",
            "(A,(B,(C D){C D}){B C D},E){A B C};",
            "(A,(B,(C D){C D}){B X D},E){A B C D E};",
        ]

        for t in bad_trees:
            with self.assertRaises(ValueError):
                PhyTree(loads(t))


if __name__ == '__main__':
    unittest.main()

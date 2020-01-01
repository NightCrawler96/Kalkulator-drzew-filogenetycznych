import unittest
from typing import Set, List

from newick import loads

from phylogenetic_trees.compare import rf_distance
from phylogenetic_trees.trees import PhyTree, bipartitions


class RFDistanceTests(unittest.TestCase):
    def test_trivial_partition(self):
        tree = PhyTree(loads("(({A},{B}){A B},{C}){A B C}"))
        partitions = [
            ({"B", "C"}, {"A"}),
            ({"A", "C"}, {"B"}),
            ({"A", "B"}, {"C"}),
        ]
        received_bipartitions: List[tuple] = bipartitions(tree)

        self.assertCountEqual(received_bipartitions, partitions)

    def test_single_bipartition(self):
        tree = PhyTree(loads("(({A},{B}){A B},({C},{D}){C D}){A B C D}"))
        partitions = [
            ({"C", "D"},{"A", "B"}),
            ({"B", "C", "D"}, {"A"}),
            ({"A", "C", "D"}, {"B"}),
            ({"A", "B", "D"}, {"C"}),
            ({"B", "C", "A"}, {"D"}),
        ]
        received_bipartitions: List[tuple] = bipartitions(tree)

        self.assertCountEqual(received_bipartitions, partitions)

    def test_two_bipartitions(self):
        tree = PhyTree(loads("(({A},{B}){A B},({C},{D}){C D},{E}){A B C D E}"))
        partitions = [
            ({"B", "C", "D", "E"}, {"A"}),
            ({"A", "C", "D", "E"}, {"B"}),
            ({"A", "B", "D", "E"}, {"C"}),
            ({"B", "C", "A", "E"}, {"D"}),
            ({"B", "C", "A", "D"}, {"E"}),
            ({"A", "B", "E"}, {"C", "D"}),
            ({"C", "D", "E"}, {"A", "B"}),
        ]

        received_bipartitions: List[tuple] = bipartitions(tree)

        self.assertCountEqual(received_bipartitions, partitions)

    def test_rf_distance_all_different_bipartitions(self):
        left_tree = PhyTree(loads("(({A},{B}){A B},({C},{D}){C D},{E}){A B C D E}"))
        right_tree = PhyTree(loads("(({A},{B},{C}){A B C},({D},{E}){D E}){A B C D E}"))

        distance: int = rf_distance(left_tree, right_tree)
        self.assertEqual(distance, 6)

    def test_rf_distance_one_common(self):
        left_tree = PhyTree(loads("(({A},{B}){A B},({C},{D}){C D},{E}){A B C D E}"))
        right_tree = PhyTree(loads("(({A},{B}){A B},({C},{D},{E}){C D E}){A B C D E}"))

        distance: int = rf_distance(left_tree, right_tree)
        self.assertEqual(distance, 2)


if __name__ == '__main__':
    unittest.main()

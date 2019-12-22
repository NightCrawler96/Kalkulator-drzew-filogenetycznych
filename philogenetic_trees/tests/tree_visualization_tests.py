import unittest

from newick import loads

from philogenetic_trees.visualization import _position_vertices


class VisualizeTree(unittest.TestCase):
    def test_two_layer_tree(self):
        tree = loads("((l1c0c0,l1c0c1)l0c0,(l1c1c0,l1c1c1)l0c1)Root;")
        positions = _position_vertices(tree[0], 1)
        space_first_layer = .5
        space_second_layer = .25
        root_position = 0

        self.assertIsInstance(positions, list)
        self.assertEqual(len(positions), 7)
        self.assertTupleEqual(positions[0], (0., root_position))
        self.assertTupleEqual(positions[1], (1., root_position + 0 * space_first_layer))
        self.assertTupleEqual(positions[2], (2., root_position + 0 * space_first_layer + 0 * space_second_layer))
        self.assertTupleEqual(positions[3], (2., root_position + 0 * space_first_layer + 1 * space_second_layer))
        self.assertTupleEqual(positions[4], (1., root_position + 1 * space_first_layer))
        self.assertTupleEqual(positions[5], (2., root_position + 1 * space_first_layer + 0 * space_second_layer))
        self.assertTupleEqual(positions[6], (2., root_position + 1 * space_first_layer + 1 * space_second_layer))

    def test_choose_positions_even_children(self):
        available_space = 1.
        children = 4
        space_per_child = available_space / children
        root_position = 0

        tree = loads("(Child0,Child1,Child2,Child3)Root;")
        positions = _position_vertices(tree[0], 1)

        self.assertIsInstance(positions, list)
        self.assertEqual(len(positions), 5)
        self.assertTupleEqual(positions[0], (0., root_position))
        self.assertTupleEqual(positions[1], (1., root_position + 0 * space_per_child))
        self.assertTupleEqual(positions[2], (1., root_position + 1 * space_per_child))
        self.assertTupleEqual(positions[3], (1., root_position + 2 * space_per_child))
        self.assertTupleEqual(positions[4], (1., root_position + 3 * space_per_child))

    def test_choose_positions_not_even_children(self):
        available_space = 1.
        children = 5
        space_per_child = available_space / children
        root_position = 0

        tree = loads("(Child0,Child1,Child2,Child3,Child4)Root;")
        positions = _position_vertices(tree[0], 1)

        self.assertIsInstance(positions, list)
        self.assertEqual(len(positions), 6)
        self.assertTupleEqual(positions[0], (0., root_position))
        self.assertTupleEqual(positions[1], (1., root_position + 0 * space_per_child))
        self.assertTupleEqual(positions[2], (1., root_position + 1 * space_per_child))
        self.assertTupleEqual(positions[3], (1., root_position + 2 * space_per_child))
        self.assertTupleEqual(positions[4], (1., root_position + 3 * space_per_child))
        self.assertTupleEqual(positions[5], (1., root_position + 4 * space_per_child))


if __name__ == '__main__':
    unittest.main()

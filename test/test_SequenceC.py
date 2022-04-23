from unittest import TestCase

import numpy as np

from app.Node import Node
from app.SequenceC import C_t

GRID_SIZE = 100

class Test(TestCase):
    def test_c_1(self):
        self.assertEqual(30613048345941659, C_t(1))

    def test_c_10(self):
        self.assertEqual(21808930308198471, C_t(10))

    def test_c_100(self):
        self.assertEqual(16190667393984172, C_t(100))

    def test_c_independent(self):

        tree = Node(-1, np.array([0, GRID_SIZE - 1, 0, GRID_SIZE - 1], dtype=np.int64))
        tree.add_child(np.array([0,1,0,1]))
        tree.add_child(np.array([2,3,2,3]))
        self.assertEqual(12 * (GRID_SIZE*GRID_SIZE - 8) + 8, tree.score())

    def test_c_contained(self):
        tree = Node(-1, np.array([0, GRID_SIZE - 1, 0, GRID_SIZE - 1], dtype=np.int64))
        tree.add_child(np.array([0,2,0,2]))
        tree.add_child(np.array([0,1,0,1]))
        self.assertEqual(12 * (GRID_SIZE*GRID_SIZE-9) + (9 - 4) + 4 * 2, tree.score())

    def test_c_intersect(self):
        tree = Node(-1, np.array([0, GRID_SIZE - 1, 0, GRID_SIZE - 1], dtype=np.int64))
        tree.add_child(np.array([0, 1, 0, 1]))
        tree.add_child(np.array([1, 2, 1, 2]))
        self.assertEqual(12 * (GRID_SIZE * GRID_SIZE - 7) + (7 - 1) + 2, tree.score())

    def test_c_contain_other_order(self):
        tree = Node(-1, np.array([0, GRID_SIZE - 1, 0, GRID_SIZE - 1], dtype=np.int64))
        tree.add_child(np.array([0, 1, 0, 1]))
        tree.add_child(np.array([0, 2, 0, 2]))
        self.assertEqual(12 * (GRID_SIZE * GRID_SIZE - 9) + (9 - 4) + 4 * 2, tree.score())

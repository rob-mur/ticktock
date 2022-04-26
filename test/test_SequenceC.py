from unittest import TestCase

import numpy as np

import app.SequenceC
from app.Node import Node
from app.SequenceC import C_t

GRID_SIZE = 100


class Test(TestCase):

    def test_c_1(self):
        self.assertEqual(30613048345941659, C_t(1))

    def test_c_2(self):
        self.assertEqual(30418584619130954, C_t(2))

    def test_c_3(self):
        self.assertEqual(27007488494046951, C_t(3))

    def test_c_4(self):
        self.assertEqual(26387001815160431, C_t(4))

    def test_c_10(self):
        self.assertEqual(21808930308198471, C_t(10))

    #def test_c_100(self):
     #   self.assertEqual(16190667393984172, C_t(100))

    def test_c_independent(self):
        tree = Node(-1, np.array([0, GRID_SIZE - 1, 0, GRID_SIZE - 1], dtype=np.int64))
        tree.add_child(Node(0, np.array([0, 1, 0, 1])))
        tree.add_child(Node(0, np.array([2, 3, 2, 3])))
        self.assertEqual(12 * (GRID_SIZE * GRID_SIZE - 8) + 8, tree.score())

    def test_c_contained(self):
        tree = Node(-1, np.array([0, GRID_SIZE - 1, 0, GRID_SIZE - 1], dtype=np.int64))
        tree.add_child(Node(0, np.array([0, 2, 0, 2])))
        tree.add_child(Node(0, np.array([0, 1, 0, 1])))
        self.assertEqual(12 * (GRID_SIZE * GRID_SIZE - 9) + (9 - 4) + 4 * 2, tree.score())

    def test_c_intersect(self):
        tree = Node(-1, np.array([0, GRID_SIZE - 1, 0, GRID_SIZE - 1], dtype=np.int64))
        tree.add_child(Node(0, np.array([0, 1, 0, 1])))
        tree.add_child(Node(0, np.array([1, 2, 1, 2])))
        self.assertEqual(12 * (GRID_SIZE * GRID_SIZE - 7) + (7 - 1) + 2, tree.score())

    def test_c_contain_other_order(self):
        tree = Node(-1, np.array([0, GRID_SIZE - 1, 0, GRID_SIZE - 1], dtype=np.int64))
        tree.add_child(Node(0, np.array([0, 1, 0, 1])))
        tree.add_child(Node(0, np.array([0, 2, 0, 2])))
        self.assertEqual(12 * (GRID_SIZE * GRID_SIZE - 9) + (9 - 4) + 4 * 2, tree.score())

    def test_contain_two(self):
        tree = Node(-1, np.array([0, GRID_SIZE - 1, 0, GRID_SIZE - 1], dtype=np.int64))
        tree.add_child(Node(0, np.array([0, 1, 0, 1])))
        tree.add_child(Node(0, np.array([0, 3, 0, 3])))
        tree.add_child(Node(0, np.array([2, 3, 2, 3])))
        self.assertEqual(12 * (GRID_SIZE * GRID_SIZE - 16) + (16 - 8) + 8 * 2, tree.score())

    def test_contain_two_almost(self):
        tree = Node(-1, np.array([0, GRID_SIZE - 1, 0, GRID_SIZE - 1], dtype=np.int64))
        tree.add_child(Node(0, np.array([0, 1, 0, 1])))
        tree.add_child(Node(0, np.array([0, 2, 0, 2])))
        tree.add_child(Node(0, np.array([2, 3, 2, 3])))
        self.assertEqual(12 * (GRID_SIZE * GRID_SIZE - 12) + 7 + 5 * 2, tree.score())

    def test_multilayer(self):
        tree = Node(-1, np.array([0, GRID_SIZE - 1, 0, GRID_SIZE - 1], dtype=np.int64))
        tree.add_child(Node(0, np.array([0, 1, 0, 1])))
        tree.add_child(Node(0, np.array([0, 1, 0, 1])))
        tree.add_child(Node(0, np.array([1, 2, 1, 2])))
        self.assertEqual(12 * (GRID_SIZE * GRID_SIZE - 7) + 3 * 2 + 3 + 3, tree.score())

    def test_pokey(self):
        tree = Node(-1, np.array([0, GRID_SIZE - 1, 0, GRID_SIZE - 1], dtype=np.int64))
        tree.add_child(Node(0, np.array([0, 2, 0, 0])))
        tree.add_child(Node(0, np.array([1, 1, 0, 1])))
        self.assertEqual(12 * (GRID_SIZE * GRID_SIZE - 4) + 3 + 2, tree.score())

    def test_both_intersect_and_contain(self):
        tree = Node(-1, np.array([0, GRID_SIZE - 1, 0, GRID_SIZE - 1], dtype=np.int64))
        tree.add_child(Node(0, np.array([0, 0, 0, 0])))
        tree.add_child(Node(0, np.array([1,3,0,0])))
        tree.add_child(Node(0, np.array([0,2,0,0])))
        self.assertEqual(12 * (GRID_SIZE * GRID_SIZE - 4) + 1 + 2*3, tree.score())

    def test_proper_overlap(self):
        tree = Node(-1, np.array([0, GRID_SIZE - 1, 0, GRID_SIZE - 1], dtype=np.int64))
        tree.add_child(Node(0, np.array([2, 3, 3, 7])))
        tree.add_child(Node(0, np.array([0, 4, 0, 4])))
        self.assertEqual(12 * (GRID_SIZE * GRID_SIZE - 31) + 27 + 8, tree.score())

    def test_problem_square(self):
        tree = Node(-1, np.array([0, app.SequenceC.GRID_SIZE - 1, 0, app.SequenceC.GRID_SIZE - 1], dtype=np.int64))
        tree.add_child(Node(0, np.array([ 3034546, 17939732, 22608053, 23794117], dtype=np.int64)))
        tree.add_child(Node(0, np.array([ 10474246, 25904962, 18236822, 38959070], dtype=np.int64)))
        self.assertEqual(12 * (app.SequenceC.GRID_SIZE * app.SequenceC.GRID_SIZE - 328583127703033) + 337437680541688, tree.score())

    def test_triple_layer_intersect(self):
        tree = Node(-1, np.array([0, GRID_SIZE - 1, 0, GRID_SIZE - 1], dtype=np.int64))
        tree.add_child(Node(0, np.array([0, 0, 0, 0])))
        tree.add_child(Node(0, np.array([0, 1, 0, 0])))
        tree.add_child(Node(0, np.array([0, 2, 0, 0])))
        self.assertEqual(12 * (GRID_SIZE * GRID_SIZE - 3) + 3 + 2 + 1, tree.score())

    def test_slug(self):
        tree = Node(-1, np.array([0, GRID_SIZE - 1, 0, GRID_SIZE - 1], dtype=np.int64))
        tree.add_child(Node(0, np.array([1, 2, 0, 1])))
        tree.add_child(Node(0, np.array([0, 1, 0, 2])))
        tree.add_child(Node(0, np.array([0, 2, 0, 1])))
        self.assertEqual(12 * (GRID_SIZE * GRID_SIZE - 8) + 16, tree.score())

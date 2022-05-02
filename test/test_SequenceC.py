from unittest import TestCase
from app.SequenceC import C

import numpy as np

import app.SequenceC
from app.Node import Node
from app.SequenceC import C_t

GRID_SIZE = 100


class Test(TestCase):

    def test_c_1(self):
        self.assertEqual(30613048345941659, C().from_s(1))

    def test_c_2(self):
        self.assertEqual(30418584619130954, C().from_s(2))

    def test_c_3(self):
        self.assertEqual(27007488494046951, C().from_s(3))

    def test_c_4(self):
        self.assertEqual(23967876580415111, C().from_s(4))

    def test_c_10(self):
        self.assertEqual(21808930308198471, C().from_s(10))

    def test_c_100(self):
       self.assertEqual(16190667393984172, C().from_s(100))

    def test_c_independent(self):
        sut = C(GRID_SIZE)
        result = sut.from_rectangles([0,1,0,1], [2,3,2,3])
        self.assertEqual(12 * (GRID_SIZE * GRID_SIZE - 8) + 8, result)

    def test_c_contained(self):
        sut = C(GRID_SIZE)
        result = sut.from_rectangles([0, 2, 0, 2], [0, 1, 0, 1])
        self.assertEqual(12 * (GRID_SIZE * GRID_SIZE - 9) + (9 - 4) + 4 * 2, result)

    def test_c_intersect(self):
        sut = C(GRID_SIZE)
        result = sut.from_rectangles([0, 1, 0, 1], [1, 2, 1, 2])
        self.assertEqual(12 * (GRID_SIZE * GRID_SIZE - 7) + (7 - 1) + 2, result)

    def test_c_contain_other_order(self):
        sut = C(GRID_SIZE)
        result = sut.from_rectangles([0, 1, 0, 1], [0, 2, 0, 2])
        self.assertEqual(12 * (GRID_SIZE * GRID_SIZE - 9) + (9 - 4) + 4 * 2, result)

    def test_contain_two(self):
        sut = C(GRID_SIZE)
        result = sut.from_rectangles([0,1,0,1],[0,3,0,3],[2,3,2,3])
        self.assertEqual(12 * (GRID_SIZE * GRID_SIZE - 16) + (16 - 8) + 8 * 2, result)

    def test_contain_two_almost(self):
        sut = C(GRID_SIZE)
        result = sut.from_rectangles([0,1,0,1],[0,2,0,2],[2,3,2,3])
        self.assertEqual(12 * (GRID_SIZE * GRID_SIZE - 12) + 7 + 5 * 2, result)

    def test_multilayer(self):
        sut = C(GRID_SIZE)
        result = sut.from_rectangles([0, 1, 0, 1], [0, 1, 0, 1], [1, 2, 1, 2])
        self.assertEqual(12 * (GRID_SIZE * GRID_SIZE - 7) + 3 * 2 + 3 + 3, result)

    def test_pokey(self):
        sut = C(GRID_SIZE)
        result = sut.from_rectangles([0,2,0,0],[1,1,0,1])
        self.assertEqual(12 * (GRID_SIZE * GRID_SIZE - 4) + 3 + 2, result)

    def test_both_intersect_and_contain(self):
        sut = C(GRID_SIZE)
        result = sut.from_rectangles([0,0,0,0],[1,3,0,0],[0,2,0,0])
        self.assertEqual(12 * (GRID_SIZE * GRID_SIZE - 4) + 1 + 2*3, result)

    def test_proper_overlap(self):
        sut = C(GRID_SIZE)
        result = sut.from_rectangles([2,3,3,7],[0,4,0,4])
        self.assertEqual(12 * (GRID_SIZE * GRID_SIZE - 31) + 27 + 8, result)

    def test_problem_square(self):
        sut = C()
        result = sut.from_rectangles([ 3034546, 17939732, 22608053, 23794117],[ 10474246, 25904962, 18236822, 38959070])
        self.assertEqual(12 * (app.SequenceC.GRID_SIZE * app.SequenceC.GRID_SIZE - 328583127703033) + 337437680541688, result)

    def test_triple_layer_intersect(self):
        sut = C(GRID_SIZE)
        result = sut.from_rectangles([0,0,0,0],[0,1,0,0],[0,2,0,0])
        self.assertEqual(12 * (GRID_SIZE * GRID_SIZE - 3) + 3 + 2 + 1, result)

    def test_slug(self):
        sut = C(GRID_SIZE)
        result = sut.from_rectangles([1,2,0,1],[0,1,0,2],[0,2,0,1])
        self.assertEqual(12 * (GRID_SIZE * GRID_SIZE - 8) + 16, result)

    def test_cross(self):
        sut = C(GRID_SIZE)
        result = sut.from_rectangles([0,2,1,1],[1,1,0,2],[0,2,0,2])
        self.assertEqual(12 * (GRID_SIZE * GRID_SIZE - 9) + 15, result)

    def test_cross_with_uneven_container(self):
        sut = C(GRID_SIZE)
        result = sut.from_rectangles([0,4,2,2],[2,2,0,4],[1,3,1,3],[2,4,0,4])
        self.assertEqual(12 * (GRID_SIZE * GRID_SIZE - 19) + 34, result)

    def test_correct_sub_tree(self):
        sut = C(GRID_SIZE)
        result = sut.from_rectangles([0,1,0,1],[0,1,1,1],[1,1,0,1],[1,2,1,2])
        self.assertEqual(12 * (GRID_SIZE * GRID_SIZE - 7) + 12, result)
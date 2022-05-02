import numpy as np
from intervaltree import intervaltree, IntervalTree, Interval
from tqdm import tqdm

from app.Node import Node
from app.SequenceS import S_t

from dataclasses import dataclass

GRID_SIZE = 50515093


def C_t(t):
    s_values = np.fromiter(S_t(t), dtype=np.int32)

    tree = Node(-1, np.array([0, GRID_SIZE - 1, 0, GRID_SIZE - 1], dtype=np.int64))

    for n in tqdm(range(1, t + 1)):
        n_values = s_values[4 * n - 4: 4 * n]
        x0 = min(n_values[0], n_values[1])
        x1 = max(n_values[0], n_values[1])
        y0 = min(n_values[2], n_values[3])
        y1 = max(n_values[2], n_values[3])
        tree.add_child(Node(0, np.array([x0, x1, y0, y1], dtype=np.int64)))
        print(f"Did iteration {n}")

    return tree.score()


@dataclass
class Rectangle:
    x0: int
    x1: int
    y0: int
    y1: int


def rectangles(t):
    iter = S_t(t)
    for i in range(0, t):
        n_0 = next(iter)
        n_1 = next(iter)
        n_2 = next(iter)
        n_3 = next(iter)
        yield Rectangle(min(n_0, n_1), max(n_0, n_1), min(n_2, n_3), max(n_2, n_3))

def rectangle_from_list(*args):
    for rectangle in args:
        yield Rectangle(rectangle[0], rectangle[1], rectangle[2], rectangle[3])


class C:

    _small_delta = 0.1

    def __init__(self, grid_size = GRID_SIZE):
        self._grid_size = grid_size

    def _analyse_rectangles(self, rectangles):
        x_tree = IntervalTree()
        elementary_x = set()
        for rect in rectangles:
            print(rect)
            if not Interval(rect.x0, rect.x1 + 1) in x_tree:
                x_tree[rect.x0: rect.x1 + 1] = [rect.y0, rect.y1 + 1]
            else:
                print("untested case happened")

            elementary_x.update([rect.x0, rect.x1 + 1])

        elementary_x = sorted(elementary_x)

        score = 0
        tot_area = 0
        for i in range(0, len(elementary_x) - 1):
            y_tree = IntervalTree()
            y_values = set()
            for interval in x_tree[elementary_x[i]:elementary_x[i + 1]]:
                y_tree.add(Interval(interval.data[0], interval.data[1]))
                y_values.update([interval.data[0], interval.data[1]])
            y_values = sorted(y_values)
            for j in range(0, len(y_values) - 1):
                overlaps = y_tree[y_values[j]:y_values[j + 1]]
                area = (elementary_x[i + 1]  - elementary_x[i]) * (y_values[j + 1]  - y_values[j])
                tot_area += area
                score += len(overlaps) % 12 * area

        return 12 * (self._grid_size * self._grid_size - tot_area) + score

    def from_s(self, t):
        return self._analyse_rectangles(rectangles(t))

    def from_rectangles(self, *args):
        generator = rectangle_from_list(*args)
        return self._analyse_rectangles(generator)

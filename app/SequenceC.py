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
        #print(f"Did iteration {n}")

    return tree.score()


@dataclass
class Rectangle:
    x0: int
    x1: int
    y0: int
    y1: int


from enum import Enum


class Boundary(Enum):
    LEFT = 1
    RIGHT = 2


@dataclass
class RectangleBoundary:
    rectangle: Rectangle
    value: int
    type: Boundary

    def __lt__(self, obj):
        return self.value < obj.value or (
                    self.value == obj.value and (self.type == Boundary.LEFT and obj.type == Boundary.RIGHT))


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


@dataclass
class StripeData:
    active_count: int = 0
    score: int = 0
    area: int = 0

    def __hash__(self):
        return id(self)


class C:

    def __init__(self, grid_size=GRID_SIZE):
        self._grid_size = grid_size

    def _analyse_rectangles(self, rectangle_iter):
        rectangles = [rectangle for rectangle in rectangle_iter]
        print("Analysing y_values")
        y_values = sorted(set([x for rect in rectangles for x in [rect.y0, rect.y1 + 1]]))
        print("Creating the squeezed rectangles")
        squeezed_rectangles = rectangles
        for rect in tqdm(squeezed_rectangles):
            rect.y0 = y_values.index(rect.y0)
            rect.y1 = y_values.index(rect.y1 + 1)

        stripes = [StripeData() for _ in range(len(y_values) - 1)]
        print("Analysing x values")
        x_values = sorted([x for rect in squeezed_rectangles for x in
                           [RectangleBoundary(rect, rect.x0, Boundary.LEFT),
                            RectangleBoundary(rect, rect.x1 + 1, Boundary.RIGHT)]])
        previous_x_value = x_values[0].value
        active_rectangles = []
        active_stripes = set()
        for x_value in tqdm(x_values):

            area = x_value.value - previous_x_value
            for overlap in active_stripes:
                if (overlap.active_count % 12) != 0:
                    overlap.area += area
                overlap.score += (overlap.active_count % 12) * area

            overlaps = stripes[x_value.rectangle.y0: x_value.rectangle.y1]
            if x_value.type == Boundary.LEFT:
                active_rectangles.append(x_value.rectangle)
                active_stripes.update(overlaps)
                for overlap in overlaps:
                    overlap.active_count += 1
            else:
                active_rectangles.remove(x_value.rectangle)
                for overlap in overlaps:
                    overlap.active_count -= 1
                    if overlap.active_count == 0:
                        active_stripes.remove(overlap)

            previous_x_value = x_value.value

        tot_area = 0
        tot_score = 0
        print("Calculating final area")
        for i, stripe in enumerate(stripes):
            height = y_values[i+1] - y_values[i]
            tot_area += stripe.area * height
            tot_score += stripe.score * height

        return 12 * (self._grid_size * self._grid_size - tot_area) + tot_score

    def from_s(self, t):
        return self._analyse_rectangles(rectangles(t))

    def from_rectangles(self, *args):
        generator = rectangle_from_list(*args)
        return self._analyse_rectangles(generator)

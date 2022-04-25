from copy import copy, deepcopy

import numpy as np


def area(bounding_box):
    return (bounding_box[1] - bounding_box[0] + 1) * (bounding_box[3] - bounding_box[2] + 1)

class Node():
    def __init__(self, level, bounding_box, children=[]):
        self.children = children
        self.level = level
        self.bounding_box = bounding_box
        self.parent = None

    def add_child(self, bounding_box):
        if self.contains(bounding_box):
            self.children = [deepcopy(self)]
            self.children[0].parent = self
            self.level += 1
            self.bounding_box = bounding_box

    def overlaps(self, bounding_box):
        return (self.bounding_box[0] <= bounding_box[1]) and (self.bounding_box[1] >= bounding_box[0]) and (self.bounding_box[2] <= bounding_box[3]) and (self.bounding_box[3] >= bounding_box[2])

    def increment_level(self):
        self.level += 1
        for child in self.children:
            child.increment_level()

    def overlap(self, bounding_box):
        x0 = max(self.bounding_box[0], bounding_box[0])
        x1 = min(self.bounding_box[1], bounding_box[1])
        y0 = max(self.bounding_box[2], bounding_box[2])
        y1 = min(self.bounding_box[3], bounding_box[3])
        return np.array([x0, x1, y0, y1], dtype=np.int64)

    def contains(self, bounding_box):
        return (bounding_box[0] >= self.bounding_box[0]) and (bounding_box[1] <= self.bounding_box[1]) and (bounding_box[2] >= self.bounding_box[2]) and (bounding_box[3] <= self.bounding_box[3])

    def is_contained_by(self, bounding_box):
        return not((self.bounding_box == bounding_box).all()) and (self.bounding_box[0] >= bounding_box[0]) and (self.bounding_box[1] <= bounding_box[1]) and (self.bounding_box[2] >= bounding_box[2]) and (self.bounding_box[3] <= bounding_box[3])

    def node_area(self):
        if self.parent:
            return area(self.bounding_box) - area(self.parent.bounding_box)
        return area(self.bounding_box)

    def score(self):
        return (self.level % 12 + 1) * self.node_area() + sum([child.score() for child in self.children])




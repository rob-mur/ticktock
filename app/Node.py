import numpy as np


def area(bounding_box):
    return (bounding_box[1] - bounding_box[0] + 1) * (bounding_box[3] - bounding_box[2] + 1)

class Node():
    def __init__(self, level, bounding_box):
        self.children = []
        self.level = level
        self.bounding_box = bounding_box
        self.dead_area = 0

    def add_child(self, bounding_box):
        dead_area = 0
        for child in self.children:
            if child.contains(bounding_box):
                child.add_child(bounding_box)
                return
            if child.overlaps(bounding_box):
                overlap = child.overlap(bounding_box)
                child.add_child(overlap)
                dead_area += area(overlap)
        new_node = Node(self.level + 1, bounding_box)
        new_node.dead_area = dead_area
        self.children.append(new_node)

    def overlaps(self, bounding_box):
        return (self.bounding_box[0] <= bounding_box[1]) and (self.bounding_box[1] >= bounding_box[0]) and (self.bounding_box[2] <= bounding_box[3]) and (self.bounding_box[3] >= bounding_box[2])

    def overlap(self, bounding_box):
        x0 = max(self.bounding_box[0], bounding_box[0])
        x1 = min(self.bounding_box[1], bounding_box[1])
        y0 = max(self.bounding_box[2], bounding_box[2])
        y1 = min(self.bounding_box[3], bounding_box[3])
        return np.array([x0, x1, y0, y1], dtype=np.int64)

    def contains(self, bounding_box):
        return (bounding_box[0] >= self.bounding_box[0]) and (bounding_box[1] <= self.bounding_box[1]) and (bounding_box[2] >= self.bounding_box[2]) and (bounding_box[3] <= self.bounding_box[3])

    def area(self):
        return area(self.bounding_box) - self.dead_area

    def score(self):
        area_of_children = sum([node.area() for node in self.children])
        score_of_children = sum([node.score() for node in self.children])
        return (self.level % 12 + 1) * (self.area() - area_of_children) + score_of_children
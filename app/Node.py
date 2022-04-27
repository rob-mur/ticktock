import numpy as np
from tqdm import tqdm


def area(bounding_box):
    return (bounding_box[1] - bounding_box[0] + 1) * (bounding_box[3] - bounding_box[2] + 1)

class Node():
    def __init__(self, level, bounding_box):
        self.children = []
        self.level = level
        self.bounding_box = bounding_box
        self.sub_nodes = set()
        self._node_area = -1
        self._node_score = -1
        self._sub_tree = set()

    def add_child(self, node):
        to_remove = []
        for child in  self.children:
            if child.is_contained_by(node.bounding_box):
                child.increment_level(node.level + 1)
                node.children.append(child)
                node.sub_nodes.add(child)
                to_remove.append(child)
                continue
            if child.contains(node.bounding_box):
                node.level += 1
                child.add_child(node)
                return
            if child.overlaps(node.bounding_box):
                overlap_area = child.overlap(node.bounding_box)
                overlap, existing = child.find_or_create(child.sub_nodes, overlap_area)
                if not existing:
                    child.add_child(overlap)
                if not node.find_or_create(node.sub_nodes, overlap_area)[1]:
                    node.add_child(overlap)

        self.children.append(node)
        self.sub_nodes.add(node)
        for dead_node in to_remove:
            self.children.remove(dead_node)

    def overlaps(self, bounding_box):
        return (self.bounding_box[0] <= bounding_box[1]) and (self.bounding_box[1] >= bounding_box[0]) and (self.bounding_box[2] <= bounding_box[3]) and (self.bounding_box[3] >= bounding_box[2])

    def increment_level(self, to):
        self.level = max(self.level, to)
        for child in self.children:
            child.increment_level(to + 1)

    def overlap(self, bounding_box):
        x0 = max(self.bounding_box[0], bounding_box[0])
        x1 = min(self.bounding_box[1], bounding_box[1])
        y0 = max(self.bounding_box[2], bounding_box[2])
        y1 = min(self.bounding_box[3], bounding_box[3])
        return np.array([x0, x1, y0, y1], dtype=np.int64)

    def contains(self, bounding_box):
        return (bounding_box[0] >= self.bounding_box[0]) and (bounding_box[1] <= self.bounding_box[1]) and (bounding_box[2] >= self.bounding_box[2]) and (bounding_box[3] <= self.bounding_box[3])

    def is_contained_by(self, bounding_box):
        return not((self.bounding_box == bounding_box ).all()) and (self.bounding_box[0] >= bounding_box[0]) and (self.bounding_box[1] <= bounding_box[1]) and (self.bounding_box[2] >= bounding_box[2]) and (self.bounding_box[3] <= bounding_box[3])

    def node_area(self):
        if self._node_area == -1:
            area_of_children = self.tree_area()
            self._node_area = area(self.bounding_box) - area_of_children
        return self._node_area

    def sub_tree(self):
        if len(self._sub_tree) == 0:
            self._sub_tree = set.union(*[child.sub_tree() for child in self.children], self.sub_nodes)
        return self._sub_tree

    def tree_area(self):
        return sum([child.node_area() for child in self.sub_tree()])

    def find_or_create(self, haystack, bounding_box):
        matches = [x for x in haystack if (x.bounding_box == bounding_box).all()]
        if len(matches) == 0:
            return Node(self.level + 1, bounding_box), False
        return matches[0], True

    def node_score(self):
        if self._node_score == -1:
            self._node_score = (self.level % 12 + 1) * self.node_area()
        return self._node_score

    def score(self):
        return (self.level % 12 + 1) * self.node_area() + sum([child.node_score() for child in self.sub_tree()])
import numpy as np


def area(bounding_box):
    return (bounding_box[1] - bounding_box[0] + 1) * (bounding_box[3] - bounding_box[2] + 1)

class Node():
    def __init__(self, level, bounding_box):
        self.children = []
        self.level = level
        self.bounding_box = bounding_box

    def add_child(self, node):
        if len([x for x in self.children if (x.bounding_box == node.bounding_box).all()]) != 0:
            return
        to_remove = []
        for child in self.children:
            if child.is_contained_by(node.bounding_box):
                if child.level == node.level:
                    child.increment_level()
                node.children.append(child)
                to_remove.append(child)
                continue
            if child.contains(node.bounding_box):
                child.add_child(node)
                return
            if child.overlaps(node.bounding_box):
                overlap = Node(child.level + 1, child.overlap(node.bounding_box))
                child.add_child(overlap)
                node.add_child(overlap)
        self.children.append(node)
        for dead_node in to_remove:
            self.children.remove(dead_node)

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
        return not((self.bounding_box == bounding_box ).all()) and (self.bounding_box[0] >= bounding_box[0]) and (self.bounding_box[1] <= bounding_box[1]) and (self.bounding_box[2] >= bounding_box[2]) and (self.bounding_box[3] <= bounding_box[3])

    def node_area(self):
        return area(self.bounding_box) - sum([child.tree_area() for child in self.children])

    def tree_area(self):
        return sum([child.node_area() for child in self.children])

    def score(self):
        area_of_children = sum([node.node_area() for node in self.children])
        score_of_children = sum([node.score() for node in self.children])
        return (self.level % 12 + 1) * (self.node_area() - area_of_children) + score_of_children
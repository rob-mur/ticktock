import numpy as np

from app.Node import Node
from app.SequenceS import S_t

GRID_SIZE = 50515093


def C_t(t):
    s_values = np.fromiter(S_t(t), dtype=np.int32)

    tree = Node(-1,np.array([0,GRID_SIZE-1,0,GRID_SIZE-1], dtype=np.int64))

    for n in range(1, t + 1):
        n_values = s_values[4 * n - 4: 4 * n]
        x0 = min(n_values[0], n_values[1])
        x1 = max(n_values[0], n_values[1])
        y0 = min(n_values[2], n_values[3])
        y1 = max(n_values[2], n_values[3])
        tree.add_child(np.array([x0, x1, y0, y1], dtype=np.int64))

    return tree.score()
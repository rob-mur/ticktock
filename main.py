import itertools
from tqdm import tqdm
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from scipy.sparse import bsr_matrix, csr_matrix
import numpy as np
from collections import defaultdict

from app.Node import area
from app.SequenceC import GRID_SIZE
from app.SequenceS import S_t
plt.figure()
currentAxis = plt.gca()
plt.xlim([0,GRID_SIZE])
plt.ylim([0,GRID_SIZE])
s_values = np.fromiter(S_t(10), dtype=np.int32)
for n in range(1,11):
    n_values = s_values[4 * n - 4: 4 * n]
    x0 = min(n_values[0], n_values[1])
    x1 = max(n_values[0], n_values[1])
    y0 = min(n_values[2], n_values[3])
    y1 = max(n_values[2], n_values[3])
    currentAxis.add_patch(Rectangle((x0,y0), x1-x0, y1-y0, fill=None, alpha=1))
    print(np.array([x0,x1,y0,y1], dtype=np.int64))
plt.show()

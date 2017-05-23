import pandas as pd
from correlation import correlation
import numpy as np
import sys

data = pd.read_csv(sys.argv[1], header=None)
labels = pd.read_csv(sys.argv[2], header=None)
lbls = []
for i in labels.values:
    lbls.append(np.mean([int(a) for a in i[1:]]))
print(correlation(data.values[:,1], lbls))

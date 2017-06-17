import pandas as pd
from correlation import correlation
import matplotlib.pyplot as plt
import numpy as np
import sys

data = pd.read_csv(sys.argv[1], header=None)
labels = pd.read_csv(sys.argv[2], header=None)
lbls = []
for i in labels.values:
    lbls.append(np.mean([int(a) for a in i[1:]]))
d = data.values[:,1]
#print(correlation(d, lbls))

plt.hist(d, bins=30, color='lightblue')
plt.xlabel('M2 measure', fontsize=18)
plt.ylabel('Number of recordings', fontsize=18)
#plt.plot(np.arange(d.shape[0]), sorted(d), linewidth=3)
plt.savefig('m2distr.jpg')


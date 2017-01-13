#!/usr/bin/env python3
import sys
import os
import pickle
import numpy as np
import glob
from observe import SavedResults
import matplotlib.pyplot as plt

fn = sys.argv[1]
means = []
fns = []
stds = []
b_width = 0.3
for dump in glob.glob('dump/*'):
    fns.append(dump.lstrip('dump/'))
    with open(dump, 'rb') as f:
        data = pickle.load(f)
        dfn = data.get_by_fn(fn)
        means.append(float(dfn[1]))
        stds.append(float(dfn[2]))
print(stds)
index = np.arange(len(fns))
plt.bar(index, means, b_width, color='blue', alpha=0.5, align='center', yerr=stds, label='MCD')
plt.xlabel('Engines used')
plt.ylabel('MCD')
plt.title('MCD value of \'{}\' for particular settings'.format(fn))
plt.xticks(index, fns)
plt.legend()

plt.tight_layout()
plt.show()

#!/usr/bin/env python3
import numpy.random as npr
import pandas as pd
import sys

data=pd.read_csv(sys.argv[1], delimiter="\t", header=None)
l=data.values.shape[0]
perm=npr.permutation(l)
with open("random_sample", "w") as f:
    for line in data.values[perm[:1000],0]:
        f.write(line+"\n")

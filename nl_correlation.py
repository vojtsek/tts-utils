#! /usr/bin/env python3
import sys
import pandas as pd
from correlation import correlation

annotated=pd.read_csv(sys.argv[1], header=None)
scored=pd.read_csv(sys.argv[2], header=None)

correlation(annotated.values[:,1], scored.values[:,1])

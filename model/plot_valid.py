import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import sys

data_train = pd.read_csv(sys.argv[1], header=None).values
data_valid = pd.read_csv(sys.argv[2], header=None).values
plt.plot(range(len(data_train)), data_train, linewidth=2)
plt.plot(range(len(data_valid)), data_valid, linewidth=2)
plt.title('Train and valid accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
gp = mpatches.Patch(color='green', label='Valid')
bp = mpatches.Patch(color='blue', label='Train')
plt.legend(handles=[gp, bp], loc=5)
plt.savefig('epochs_valid_train_gold.jpg')

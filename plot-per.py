#! /usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

best_positions = [32, 14, 15,  6, 11, 10,  6,  0,  4]
best_positions2 = [49, 26, 10,  9,  4, 0, 0, 0, 0]
index = 1 + np.arange(len(best_positions))
b_width= 0.4
plt.bar(index, best_positions, b_width, color='blue', alpha=0.5, align='center', label='Distribution of best hypothesis - 9 best')
plt.bar(index + b_width, best_positions2, b_width, color='green', alpha=0.5, align='center', label='Distribution of best hypothesis - 5 best')
plt.xticks(index, index)
plt.xlabel('Position in nbest list.')
plt.ylabel('Count of best')
plt.legend()
plt.tight_layout()
plt.show()


PERs = [61.472527472527474, 60.70329670329671, 60.1978021978022, 60.10989010989011, 59.692307692307686, 59.47252747252747, 59.38461538461538, 59.31868131868132, 59.23076923076923, 59.16483516483516]
index = 1 + np.arange(len(PERs))
plt.plot(index, PERs, linewidth=2)
plt.xlabel('Size of the nbest list.')
plt.ylabel('Phoneme Error Rate')
plt.legend()
plt.tight_layout()
plt.show()


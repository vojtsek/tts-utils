import numpy as np
import glob
import math

DIM=1100
BATCH_SIZE=64

class MGCDataset:

    def __init__(self, examples_dir, gold_dir, order=35):
        self.order = order
        x_files =  glob.glob(examples_dir+"/*.mgc")
        y_files =  glob.glob(gold_dir+"/*.mgc")
        assert len(x_files) == len(y_files)
        self.trainX = np.zeros((len(x_files), DIM, order))
        self.trainY = np.zeros((len(y_files), DIM, order))
        self.testX = np.zeros((len(x_files), DIM, order))
        self.testY = np.zeros((len(y_files), DIM, order))
        for i, (xf,yf) in enumerate(zip(x_files, y_files)):
            if i < 100:
                self.append_ex(i, xf, self.trainX)
                self.append_ex(i, yf, self.trainY)
            if i > 100:
                self.append_ex(i, xf, self.testX)
                self.append_ex(i, xf, self.testX)
                self.append_ex(i, yf, self.testY)
                self.append_ex(i, yf, self.testY)
            if i > 132:
                break
        self.no_examples = self.trainX.shape[0]
        self.no_batches = math.ceil(self.no_examples / BATCH_SIZE)
        self.current_batch = 0
        # TODO: remove over-batch examples

    def append_ex(self, i, fn, obj):
        with open(fn, "rb") as f:
            data = np.fromfile(f, dtype="float32").reshape(-1, self.order)
            l = data.shape[0]
            diff = DIM - l
            add = np.zeros((diff, self.order))
            data = np.append(data, add, axis=0)
            obj[i] = data

    def next_batch(self):
        idx = self.current_batch * BATCH_SIZE
        self.current_batch = (self.current_batch + 1) % self.no_batches
        if idx + BATCH_SIZE > self.no_examples:
            idx = self.current_batch * BATCH_SIZE
        return self.trainX[idx:(idx + BATCH_SIZE),:,:], self.trainY[idx:(idx + BATCH_SIZE),:,:]

    def get_test(self):
        return self.testX[:64,:,:], self.testY[:64,:,:]
